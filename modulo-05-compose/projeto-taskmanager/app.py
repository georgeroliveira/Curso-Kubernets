import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import redis
import json
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Configuracoes
DATABASE_URL = os.getenv('DATABASE_URL')
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
INSTANCE_ID = os.getenv('INSTANCE_ID', 'unknown')
INSTANCE_NAME = os.getenv('INSTANCE_NAME', 'Unknown Instance')

# Startup time
STARTUP_TIME = datetime.now()

# Conexao Redis
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    print(f"[{INSTANCE_ID}] Redis connected successfully!")
except Exception as e:
    print(f"[{INSTANCE_ID}] Redis connection failed: {e}")
    redis_client = None

def get_db():
    """Retorna conexao com o banco"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

@app.route('/health')
def health():
    """Health check detalhado"""
    start_time = time.time()
    
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime_seconds': (datetime.now() - STARTUP_TIME).total_seconds(),
        'instance': {
            'id': INSTANCE_ID,
            'name': INSTANCE_NAME,
            'started_at': STARTUP_TIME.isoformat()
        },
        'checks': {},
        'metrics': {}
    }
    
    # Check 1: PostgreSQL
    db_start = time.time()
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT 1 as health_check')
        result = cur.fetchone()
        
        # Contar tarefas no banco
        cur.execute('SELECT COUNT(*) as total FROM tasks')
        task_count = cur.fetchone()
        
        cur.close()
        conn.close()
        
        health_status['checks']['database'] = {
            'status': 'healthy',
            'response_time_ms': round((time.time() - db_start) * 1000, 2),
            'tasks_count': task_count['total'] if task_count else 0
        }
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'error': str(e),
            'response_time_ms': round((time.time() - db_start) * 1000, 2)
        }
    
    # Check 2: Redis
    redis_start = time.time()
    try:
        if redis_client:
            redis_client.ping()
            
            # Info do Redis
            info = redis_client.info('stats')
            
            health_status['checks']['redis'] = {
                'status': 'healthy',
                'response_time_ms': round((time.time() - redis_start) * 1000, 2),
                'total_commands': info.get('total_commands_processed', 0),
                'connected_clients': info.get('connected_clients', 0)
            }
        else:
            health_status['checks']['redis'] = {
                'status': 'not_configured',
                'message': 'Redis client not initialized'
            }
    except Exception as e:
        health_status['checks']['redis'] = {
            'status': 'unhealthy',
            'error': str(e),
            'response_time_ms': round((time.time() - redis_start) * 1000, 2)
        }
    
    # Check 3: Disco (opcional)
    try:
        import shutil
        disk = shutil.disk_usage('/app')
        health_status['checks']['disk'] = {
            'status': 'healthy',
            'total_gb': round(disk.total / (1024**3), 2),
            'used_gb': round(disk.used / (1024**3), 2),
            'free_gb': round(disk.free / (1024**3), 2),
            'percent_used': round((disk.used / disk.total) * 100, 2)
        }
    except Exception as e:
        health_status['checks']['disk'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # Metricas gerais
    health_status['metrics']['total_response_time_ms'] = round((time.time() - start_time) * 1000, 2)
    
    # Status final
    unhealthy_checks = [k for k, v in health_status['checks'].items() 
                       if isinstance(v, dict) and v.get('status') == 'unhealthy']
    
    if unhealthy_checks:
        health_status['status'] = 'unhealthy'
        health_status['unhealthy_services'] = unhealthy_checks
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code

@app.route('/ready')
def readiness():
    """Readiness probe - verifica se pode receber trafego"""
    try:
        # Verificar apenas se consegue conectar nos servicos essenciais
        conn = get_db()
        conn.close()
        
        if redis_client:
            redis_client.ping()
        
        return jsonify({
            'status': 'ready',
            'instance': INSTANCE_ID
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'not_ready',
            'error': str(e)
        }), 503

@app.route('/live')
def liveness():
    """Liveness probe - verifica se esta vivo (nao travado)"""
    return jsonify({
        'status': 'alive',
        'instance': INSTANCE_ID,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/')
def index():
    """Pagina principal com cache"""
    user_id = 1  # Simplificado - em producao viria da sessao
    
    # Tentar buscar do cache
    cache_key = f"tasks:user:{user_id}"
    if redis_client:
        try:
            cached_tasks = redis_client.get(cache_key)
            if cached_tasks:
                tasks = json.loads(cached_tasks)
                print(f"[{INSTANCE_ID}] Tasks loaded from cache")
                return render_template('index.html', tasks=tasks, from_cache=True, instance_id=INSTANCE_ID)
        except Exception as e:
            print(f"[{INSTANCE_ID}] Cache error: {e}")
    
    # Buscar do banco
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            SELECT id, title, description, completed, created_at 
            FROM tasks 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        ''', (user_id,))
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        
        # Salvar no cache por 5 minutos
        if redis_client:
            try:
                redis_client.setex(cache_key, 300, json.dumps(tasks, default=str))
                print(f"[{INSTANCE_ID}] Tasks saved to cache")
            except Exception as e:
                print(f"[{INSTANCE_ID}] Cache save error: {e}")
        
        return render_template('index.html', tasks=tasks, from_cache=False, instance_id=INSTANCE_ID)
    except Exception as e:
        print(f"[{INSTANCE_ID}] Database error: {e}")
        return f"Error loading tasks: {e}", 500

@app.route('/add', methods=['POST'])
def add_task():
    """Adicionar nova tarefa"""
    user_id = 1  # Simplificado
    title = request.form.get('title')
    description = request.form.get('description', '')
    
    if not title:
        return redirect(url_for('index'))
    
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO tasks (user_id, title, description, completed)
            VALUES (%s, %s, %s, %s)
        ''', (user_id, title, description, False))
        conn.commit()
        cur.close()
        conn.close()
        
        # Invalidar cache
        if redis_client:
            cache_key = f"tasks:user:{user_id}"
            redis_client.delete(cache_key)
            print(f"[{INSTANCE_ID}] Cache invalidated")
        
        return redirect(url_for('index'))
    except Exception as e:
        print(f"[{INSTANCE_ID}] Error adding task: {e}")
        return f"Error: {e}", 500

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    """Marcar tarefa como completa"""
    user_id = 1
    
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            UPDATE tasks 
            SET completed = NOT completed, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND user_id = %s
        ''', (task_id, user_id))
        conn.commit()
        cur.close()
        conn.close()
        
        # Invalidar cache
        if redis_client:
            cache_key = f"tasks:user:{user_id}"
            redis_client.delete(cache_key)
        
        return redirect(url_for('index'))
    except Exception as e:
        print(f"[{INSTANCE_ID}] Error updating task: {e}")
        return f"Error: {e}", 500

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Deletar tarefa"""
    user_id = 1
    
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = %s AND user_id = %s', (task_id, user_id))
        conn.commit()
        cur.close()
        conn.close()
        
        # Invalidar cache
        if redis_client:
            cache_key = f"tasks:user:{user_id}"
            redis_client.delete(cache_key)
        
        return redirect(url_for('index'))
    except Exception as e:
        print(f"[{INSTANCE_ID}] Error deleting task: {e}")
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)