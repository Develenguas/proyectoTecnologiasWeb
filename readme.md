# 📋 Task Manager API - Sistema de Gestión de Tareas

## 📖 Descripción del Proyecto

**Task Manager API** es un sistema completo de gestión de tareas desarrollado con arquitectura de microservicios. Incluye una API REST construida con Flask, una interfaz web interactiva y una base de datos MySQL, todo orquestado con Docker Compose.

### Características principales:
- ✅ API REST completa con operaciones CRUD para tareas
- ✅ Interfaz web moderna con Vanilla JavaScript
- ✅ Base de datos MySQL 8.0 para persistencia
- ✅ Sistema de prioridades (baja, media, alta) y estados (pendiente/completada)
- ✅ Filtros avanzados por prioridad y estado
- ✅ Log de operaciones en tiempo real

### Tecnologías utilizadas:
- **Backend**: Python 3.11 + Flask + SQLAlchemy
- **Base de Datos**: MySQL 8.0
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Servidor Web**: Nginx
- **Containerización**: Docker & Docker Compose

## 🚀 Instrucciones para Levantar el Proyecto

### Prerrequisitos
- **Docker** (versión 20.10 o superior)
- **Docker Compose** (versión 2.0 o superior)

### Pasos de instalación

#### 1. Asegurarse de tener la estructura de archivos
```
task-manager-api/
├── api/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

#### 2. Construir y levantar los contenedores
```bash
# Ejecutar en primer plano (ver logs)
docker-compose up --build

# O ejecutar en segundo plano
docker-compose up -d --build
```

#### 3. Acceder a la aplicación
- **Frontend (Interfaz Web)**: http://localhost:8080
- **API REST**: http://localhost:5000
- **Documentación API**: http://localhost:5000/

#### 4. Detener los contenedores
```bash
# Detener servicios manteniendo datos
docker-compose down

# Detener y eliminar volúmenes (datos)
docker-compose down -v
```

## 📡 Endpoints Disponibles

### Base URL: `http://localhost:5000/api`

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| **GET** | `/tasks` | Listar todas las tareas | `?completed=true/false`, `?priority=baja/media/alta` |
| **GET** | `/tasks/{id}` | Obtener tarea por ID | `id` (entero) |
| **POST** | `/tasks` | Crear nueva tarea | JSON en body |
| **PUT** | `/tasks/{id}` | Actualizar tarea | JSON en body |
| **DELETE** | `/tasks/{id}` | Eliminar tarea | `id` (entero) |
| **GET** | `/health` | Verificar estado del sistema | - |

### Estructura JSON para tareas:
```json
{
  "title": "Título de la tarea",
  "description": "Descripción detallada",
  "priority": "baja|media|alta",
  "completed": true/false
}
```

### Ejemplos con cURL:
```bash
# Listar tareas
curl http://localhost:5000/api/tasks

# Crear tarea
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudiar Docker", "priority": "alta"}'

# Actualizar tarea
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

## 📄 Licencia y Derechos de Autor

Copyright © 2024 [Tu Nombre]

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo LICENSE para más detalles.

---

*Desarrollado para el aprendizaje de tecnologías web modernas*