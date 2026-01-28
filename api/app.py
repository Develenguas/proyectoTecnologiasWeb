from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
import time

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos MySQL
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'rootpassword')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'taskdb')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== MODELO DE DATOS ====================
class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='media')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Esperar a que MySQL esté listo y crear las tablas
def init_db():
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            with app.app_context():
                db.create_all()
                print("✓ Base de datos MySQL inicializada correctamente")
                return True
        except Exception as e:
            retry_count += 1
            print(f"Esperando a MySQL... intento {retry_count}/{max_retries}")
            time.sleep(2)
    
    print("✗ No se pudo conectar a MySQL")
    return False

# ==================== ENDPOINTS ====================

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'API REST de Gestión de Tareas',
        'version': '1.0.0',
        'endpoints': {
            'GET /api/tasks': 'Listar todas las tareas',
            'GET /api/tasks/<id>': 'Obtener una tarea por ID',
            'POST /api/tasks': 'Crear nueva tarea',
            'PUT /api/tasks/<id>': 'Actualizar tarea',
            'DELETE /api/tasks/<id>': 'Eliminar tarea'
        }
    }), 200

# ENDPOINT 1: GET /api/tasks - Listar todas las tareas
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        completed = request.args.get('completed')
        priority = request.args.get('priority')
        
        query = Task.query
        
        if completed is not None:
            completed_bool = completed.lower() == 'true'
            query = query.filter_by(completed=completed_bool)
        
        if priority:
            query = query.filter_by(priority=priority)
        
        tasks = query.order_by(Task.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'count': len(tasks),
            'tasks': [task.to_dict() for task in tasks]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ENDPOINT 2: GET /api/tasks/<id> - Obtener tarea por ID
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({
                'success': False,
                'error': f'Tarea con ID {task_id} no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ENDPOINT 3: POST /api/tasks - Crear nueva tarea
@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({
                'success': False,
                'error': 'El campo "title" es obligatorio'
            }), 400
        
        if not data['title'].strip():
            return jsonify({
                'success': False,
                'error': 'El título no puede estar vacío'
            }), 400
        
        valid_priorities = ['baja', 'media', 'alta']
        priority = data.get('priority', 'media').lower()
        if priority not in valid_priorities:
            return jsonify({
                'success': False,
                'error': f'Prioridad inválida. Valores: {", ".join(valid_priorities)}'
            }), 400
        
        new_task = Task(
            title=data['title'].strip(),
            description=data.get('description', '').strip(),
            completed=data.get('completed', False),
            priority=priority
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tarea creada exitosamente',
            'task': new_task.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ENDPOINT 4: PUT /api/tasks/<id> - Actualizar tarea
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({
                'success': False,
                'error': f'Tarea con ID {task_id} no encontrada'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se enviaron datos para actualizar'
            }), 400
        
        if 'title' in data:
            if not data['title'].strip():
                return jsonify({
                    'success': False,
                    'error': 'El título no puede estar vacío'
                }), 400
            task.title = data['title'].strip()
        
        if 'priority' in data:
            valid_priorities = ['baja', 'media', 'alta']
            priority = data['priority'].lower()
            if priority not in valid_priorities:
                return jsonify({
                    'success': False,
                    'error': f'Prioridad inválida. Valores: {", ".join(valid_priorities)}'
                }), 400
            task.priority = priority
        
        if 'description' in data:
            task.description = data['description'].strip()
        
        if 'completed' in data:
            task.completed = bool(data['completed'])
        
        task.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tarea actualizada exitosamente',
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ENDPOINT 5: DELETE /api/tasks/<id> - Eliminar tarea
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({
                'success': False,
                'error': f'Tarea con ID {task_id} no encontrada'
            }), 404
        
        task_data = task.to_dict()
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tarea eliminada exitosamente',
            'deleted_task': task_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500

@app.route('/health', methods=['GET'])
def health():
    try:
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)