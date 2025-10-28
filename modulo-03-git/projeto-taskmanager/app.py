from flask import Flask, render_template, request, redirect, url_for, jsonify
import logging
from datetime import datetime
from dotenv import load_dotenv
from config import get_config

# Carregar variáveis de ambiente
load_dotenv()

# Configurar aplicação
app = Flask(__name__)
config = get_config()

# Configurar logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Dados em memória (será substituído por banco no módulo 5)
tasks = []
next_id = 1

@app.route('/')
def index():
    logger.info(f"Página inicial acessada - {len(tasks)} tarefas")
    return render_template('index.html', 
                         tasks=tasks, 
                         version=config.VERSION,
                         environment=config.ENVIRONMENT)

@app.route('/health')
def health():
    """Health check endpoint para monitoramento"""
    health_status = {
        "status": "healthy",
        "service": "taskmanager",
        "version": config.VERSION,
        "environment": config.ENVIRONMENT,
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "app": "ok",
            "config": "loaded",
            "tasks_count": len(tasks)
        }
    }
    logger.debug("Health check solicitado")
    return jsonify(health_status)

@app.route('/add', methods=['POST'])
def add_task():
    global next_id
    
    title = request.form.get('title')
    if title:
        task = {
            'id': next_id,
            'title': title,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        tasks.append(task)
        logger.info(f"Tarefa criada: ID={next_id}, Título='{title}'")
        next_id += 1
    
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            task['completed_at'] = datetime.now().isoformat()
            logger.info(f"Tarefa {task_id} marcada como concluída")
            break
    
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    initial_count = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]
    
    if len(tasks) < initial_count:
        logger.info(f"Tarefa {task_id} deletada")
    
    return redirect(url_for('index'))

# API endpoints para integração futura
@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    logger.debug(f"API: Listando {len(tasks)} tarefas")
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    global next_id
    
    data = request.get_json()
    if not data or 'title' not in data:
        logger.warning("API: Tentativa de criar tarefa sem título")
        return jsonify({'error': 'Title required'}), 400
    
    task = {
        'id': next_id,
        'title': data['title'],
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    tasks.append(task)
    logger.info(f"API: Tarefa criada - ID={next_id}")
    next_id += 1
    
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        logger.warning(f"API: Tarefa {task_id} não encontrada")
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    if 'completed' in data:
        task['completed'] = bool(data['completed'])
        if task['completed']:
            task['completed_at'] = datetime.now().isoformat()
        logger.info(f"API: Tarefa {task_id} atualizada")
    
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    global tasks
    initial_count = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]
    
    if len(tasks) < initial_count:
        logger.info(f"API: Tarefa {task_id} deletada")
        return '', 204
    
    logger.warning(f"API: Tarefa {task_id} não encontrada para deletar")
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    logger.info(f"TaskManager v{config.VERSION} iniciando...")
    logger.info(f"Ambiente: {config.ENVIRONMENT}")
    logger.info(f"Servidor: http://{config.HOST}:{config.PORT}")
    
    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )