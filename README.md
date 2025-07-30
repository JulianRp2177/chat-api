# 🧩 Chat Message Processor API

**API RESTful construida con FastAPI** para la recepción, validación, procesamiento y almacenamiento de mensajes de chat. Permite la conexión en tiempo real mediante WebSocket y está diseñada con buenas prácticas de desarrollo, pruebas automatizadas y arquitectura limpia.

---

## 🚀 Tecnologías utilizadas

- 🐍 Python 3.10+
- ⚡ FastAPI
- 🐢 Tortoise ORM
- 💾 SQLite
- 🧪 Pytest
- 🧪 httpx
- 🐳 Docker + Docker Compose
- 📄 .env para configuración
- 🐞 `debugpy` para depuración remota

---

## 📂 Estructura del proyecto


```
chat-api/
├── app/
│ ├── api/** endpoints y rutas 
│ ├── core/ # Configuración general, logging y handlers de errores
│ ├── repositories/ # Acceso a base de datos usando Tortoise ORM
│ ├── schemas/ # Esquemas Pydantic para validaciones de entrada/salida
│ ├── services/ # Lógica de negocio
│ ├── utils/ # Funciones auxiliares (validación, metadatos, etc.)
│ ├── debugger.py # Inicializador condicional del depurador
│ └── main.py # Punto de entrada de la aplicación FastAPI
├── docker/ # Archivos de configuración para contenedores
│ ├── Dockerfile # Imagen base para contenedor
│ └── docker-compose.yml # Orquestador de contenedores
├── tests/ # Pruebas unitarias y de integración
├── requirements.txt # Dependencias del proyecto
└── README.md
```

---

## 🛠️ Instalación local

### 1. Clona el repositorio

```
git clone https://github.com/JulianRp2177/chat-api.git
cd chat-api
```
### 2. Crea y activa un entorno virtual

```
python3 -m venv venv
source venv/bin/activate  

```

### 3. Instala las dependencias

```
pip install -r requirements.txt

```

### 4. Crea el archivo .env en la raíz del proyecto
Este archivo es requerido para que la aplicación funcione correctamente
```
ENV=dev
WEB_APP_TITLE=Chat Message Processor API
WEB_APP_DESCRIPTION=API REST para recepción, validación y almacenamiento de mensajes.
WEB_APP_VERSION=1.0.0
DATABASE_URL=sqlite://db.sqlite3
API_KEY=mysecret123
DEBUGGER=False
```


### 5. 🐳 Ejecución con Docker
Debes tener instalado:

-   Docker

-   Docker Compose

Si no lo tienes, puedes instalarlo desde: https://docs.docker.com/get-docker/

 Ejecutar con Docker Compose

```
docker compose -f docker/Docker-compose.yml up --build
```
🔗 Accede a la documentación Swagger en http://localhost:8001/docs

Esto levantará un contenedor con FastAPI y base de datos SQLite.

---

## 🧪 Ejecutar pruebas

### 1. Activa tu entorno virtual

```
source venv/bin/activate
```
### 2. Ejecuta todos los tests desde la terminal

```
pytest
```

### 3. Con reporte de cobertura
```
pytest --cov=app --cov-report=term-missing
```
---

## 🐞 Debugging remoto con debugpy (modo seguro)
La aplicación permite activar el debugger debugpy para conectarte desde VS Code de manera segura y controlada.

### ✅ ¿Cómo activarlo?
En el archivo .env, establece la variable:

```
DEBUGGER=True
```

Al iniciar la aplicación, si el proceso cumple las condiciones de seguridad, verás:
```
⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳
```

- Tener en cuenta en la raiz del proyecto hay un archivo launch.json con la configuracion debe copiarse a la carpeta .vscode del depurador creando un archivo Python Debugger

---

## 📄 Licencia

MIT © 2025 - JULIAN RODRIGUEZ