import os
import time
import json
import logging
from datetime import datetime
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for, jsonify
import redis

# Configuração de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Configurações
DATABASE_URL = os.getenv('DATABASE_URL')
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
INSTANCE_ID = os.getenv('INSTANCE_ID', 'unknown')
INSTANCE_NAME = os.getenv('INSTANCE_NAME', 'Unknown Instance')
STARTUP_TIME = datetime.now()

# Conexão Redis
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info(f"[{INSTANCE_ID}] Redis connected successfully!")
except Exception as e:
    logger.warning(f"[{INSTANCE_ID}] Redis connection failed: {e}")
    redis_client = None

def get_db():
    """Retorna conexão com o banco com Retry Logic"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            # Tenta conectar
            conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
            return conn
        except OperationalError as e:
            if attempt == max_retries - 1:
                logger.error(f"Falha final ao conectar no DB: {e}")
                raise e
            logger.warning(f"Banco indisponível, tentando novamente em {retry_delay}s... ({attempt+1}/{max_retries})")
            time.sleep(retry_delay)

@app.route('/health')
def health():
    """Health check detalhado"""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime_seconds': (datetime.now() - STARTUP_TIME).total_seconds(),
        'instance': {
            'id': INSTANCE_ID,
            'name': INSTANCE_NAME
        },
        'checks': {}
    }
    
    # Check DB
    try:
        conn = get_db()
        conn.close()
        health_status['checks']['database'] = 'healthy'
    except Exception as e:
        health_status['checks']['database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'

    # Check Redis
    if redis_client:
        try:
            redis_client.ping()
            health_status['checks']['redis'] = 'healthy'
        except Exception as e:
            health_status['checks']['redis'] = f'unhealthy: {str(e)}'
            health_status['status'] = 'unhealthy'
    else:
        health_status['checks']['redis'] = 'not_configured'

    return jsonify(health_status)

@app.route('/ready')
def readiness():
    """Readiness probe - verifica se pode receber trafego"""
    try:
        conn = get_db()
        conn.close()
        if redis_client:
            redis_client.ping()
        return jsonify({'status': 'ready', 'instance': INSTANCE_ID}), 200
    except Exception as e:
        return jsonify({'status': 'not_ready', 'error': str(e)}), 503

@app.route('/live')
def liveness():
    """Liveness probe - verifica se esta vivo"""
    return jsonify({
        'status': 'alive',
        'instance': INSTANCE_ID,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/')
def index():
    """Pagina principal com cache"""
    user_id = 1  # Simplificado
    
    # Tentar buscar do cache
    cache_key = f"tasks:user:{user_id}"
    if redis_client:
        try:
            cached_tasks = redis_client.get(cache_key)
            if cached_tasks:
                tasks = json.loads(cached_tasks)
                logger.info(f"[{INSTANCE_ID}] Tasks loaded from cache")
                return render_template('index.html', tasks=tasks, from_cache=True, instance_id=INSTANCE_ID)
        except Exception as e:
            logger.error(f"[{INSTANCE_ID}] Cache error: {e}")
    
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
                logger.info(f"[{INSTANCE_ID}] Tasks saved to cache")
            except Exception as e:
                logger.error(f"[{INSTANCE_ID}] Cache save error: {e}")
        
        return render_template('index.html', tasks=tasks, from_cache=False, instance_id=INSTANCE_ID)
    except Exception as e:
        logger.error(f"[{INSTANCE_ID}] Database error: {e}")
        return f"Error loading tasks: {e}", 500

@app.route('/add', methods=['POST'])
def add_task():
    """Adicionar nova tarefa"""
    user_id = 1
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
            logger.info(f"[{INSTANCE_ID}] Cache invalidated")
        
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"[{INSTANCE_ID}] Error adding task: {e}")
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
        
        if redis_client:
            cache_key = f"tasks:user:{user_id}"
            redis_client.delete(cache_key)
        
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"[{INSTANCE_ID}] Error updating task: {e}")
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
        
        if redis_client:
            cache_key = f"tasks:user:{user_id}"
            redis_client.delete(cache_key)
        
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"[{INSTANCE_ID}] Error deleting task: {e}")
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)