# 📋 API REST - Gestor de Tareas

Sistema de gestión de tareas desarrollado con Flask, PostgreSQL y Docker. Incluye API REST completa y una interfaz web para administrar tareas.

## 🚀 Tecnologías Utilizadas

- **Backend**: Python 3.11 + Flask
- **Base de Datos**: PostgreSQL 15
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Servidor Web**: Nginx
- **Containerización**: Docker & Docker Compose

## 📁 Estructura del Proyecto
```
task-manager-api/
│
├── api/                      # Contenedor 1: API REST
│   ├── app.py               # Aplicación Flask
│   ├── requirements.txt     # Dependencias Python
│   └── Dockerfile          # Imagen Docker de la API
│
├── frontend/                 # Contenedor 3: Interfaz Web
│   ├── index.html           # UI del gestor de tareas
│   ├── nginx.conf           # Configuración Nginx
│   └── Dockerfile          # Imagen Docker del frontend
│
├── docker-compose.yml       # Orquestación de servicios
├── .env                     # Variables de entorno
└── README.md               # Documentación
```

## 🔧 Requisitos Previos

- Docker (versión 20.10 o superior)
- Docker Compose (versión 2.0 o superior)

## 📦 Instalación y Ejecución

### 1. Clonar o descargar el proyecto
```bash
cd task-manager-api
```

### 2. Configurar variables de entorno (opcional)

Edita el archivo `.env` si deseas cambiar las credenciales:
```env
DB_USER=postgres
DB_PASSWORD=postgres123
DB_NAME=taskdb
```

### 3. Construir y levantar los contenedores
```bash
docker-compose up --build
```

O en segundo plano:
```bash
docker-compose up -d --build
```

### 4. Acceder a la aplicación

- **Frontend (Interfaz Web)**: http://localhost:8080
- **API REST**: http://localhost:5000
- **Documentación API**: http://localhost:5000/

### 5. Detener los contenedores
```bash
docker-compose down
```

Para eliminar también los volúmenes (datos):
```bash
docker-compose down -v
```

## 📡 Endpoints de la API

### Base URL: `http://localhost:5000/api`

| Método | Endpoint | Descripción | Body (JSON) |
|--------|----------|-------------|-------------|
| GET | `/tasks` | Listar todas las tareas | - |
| GET | `/tasks/<id>` | Obtener tarea por ID | - |
| POST | `/tasks` | Crear nueva tarea | `{"title": "string", "description": "string", "priority": "baja\|media\|alta"}` |
| PUT | `/tasks/<id>` | Actualizar tarea | `{"title": "string", "description": "string", "priority": "string", "completed": boolean}` |
| DELETE | `/tasks/<id>` | Eliminar tarea | - |

### Filtros disponibles (GET /tasks)

- `?completed=true/false` - Filtrar por estado
- `?priority=baja/media/alta` - Filtrar por prioridad

### Ejemplos de uso con cURL

**Listar todas las tareas:**
```bash
curl http://localhost:5000/api/tasks
```

**Crear una nueva tarea:**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudiar Docker",
    "description": "Aprender contenedores y orquestación",
    "priority": "alta"
  }'
```

**Obtener tarea por ID:**
```bash
curl http://localhost:5000/api/tasks/1
```

**Actualizar tarea:**
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true,
    "priority": "media"
  }'
```

**Eliminar tarea:**
```bash
curl -X DELETE http://localhost:5000/api/tasks/1
```

## 🐳 Arquitectura Docker

El proyecto utiliza 3 contenedores:

1. **task_database** (PostgreSQL)
   - Puerto: 5432 (interno)
   - Volumen: `postgres_data` para persistencia

2. **task_api** (Flask)
   - Puerto: 5000
   - Conecta con la base de datos

3. **task_frontend** (Nginx)
   - Puerto: 8080
   - Sirve la interfaz web

Todos los contenedores están conectados mediante la red `task_network`.

## 📊 Modelo de Datos

**Tabla: tasks**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | ID único (clave primaria) |
| title | String(200) | Título de la tarea |
| description | Text | Descripción detallada |
| completed | Boolean | Estado (completada/pendiente) |
| priority | String(20) | Prioridad (baja/media/alta) |
| created_at | DateTime | Fecha de creación |
| updated_at | DateTime | Última actualización |

## 🛠️ Comandos Útiles

**Ver logs de todos los servicios:**
```bash
docker-compose logs -f
```

**Ver logs de un servicio específico:**
```bash
docker-compose logs -f api
```

**Reiniciar un servicio:**
```bash
docker-compose restart api
```

**Ver estado de los contenedores:**
```bash
docker-compose ps
```

**Acceder al contenedor de la API:**
```bash
docker exec -it task_api sh
```

**Acceder a PostgreSQL:**
```bash
docker exec -it task_database psql -U postgres -d taskdb
```

## 🔍 Verificación de Funcionamiento

1. **Verificar que los contenedores están corriendo:**
```bash
   docker-compose ps
```

2. **Probar la API:**
```bash
   curl http://localhost:5000/health
```

3. **Abrir el frontend:**
   - Navega a http://localhost:8080

## 🐛 Solución de Problemas

**Error: Puerto ya en uso**
- Cambia los puertos en `docker-compose.yml`

**Error: No se puede conectar a la base de datos**
- Espera a que PostgreSQL esté completamente iniciado
- Verifica las variables de entorno en `.env`

**Frontend no carga datos**
- Verifica que la API esté corriendo en http://localhost:5000
- Revisa la consola del navegador para errores CORS

## 👨‍💻 Autor

Proyecto desarrollado como práctica de API REST con Docker

## 📄 Licencia

Este proyecto es de uso educativo y libre.