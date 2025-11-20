# AI Service

Servicio de IA encargado de:
- Generar audios (TTS) y subirlos a Google Cloud Storage.
- Generar historias, ejercicios u otros recursos usando modelos de IA.
- Exponer endpoints consumidos por el API Gateway.

Link del repositorio en GitHub: https://github.com/Creative-Craft-UPC/ai-service 

---

## Clonar el Repositorio

```bash
git clone https://github.com/Creative-Craft-UPC/ai-service.git
cd social_fun
```

## 🧱 Stack tecnológico

- Python 3.11
- FastAPI
- Uvicorn
- Google Cloud Storage (GCS)
- PyJWT (token interno desde el Gateway)
- Docker + Cloud Run
- python-dotenv

---

## 📁 Estructura básica

- `main.py` → punto de entrada FastAPI
- `routes/` → rutas HTTP (por ejemplo `prompt_routes.py`)
- `services/` → integración con IA, GCS, etc.
- `auth/internal_dep.py` → validación de token interno (JWT RS256)
- `requirements.txt` → dependencias de Python
- `Dockerfile` → build de imagen

---

## ⚙️ Variables de entorno

Ejemplo de variables necesarias (.env):

### IA / OpenAI / proveedor
API_KEY=...

### Google Cloud Storage
GCS_BUCKET_NAME=...

### Seguridad (JWT interno)
PUBLIC_KEY_PATH=/app/secrets/bff_public.pem

### Base de datos
MONGO_URI=...

---

## Ejecución:
### 🚀 Ejecutar en local (sin Docker)

1. Crear entorno virtual y activalo:

    python -m venv aiContext

    aiContext/Scripts/activate ---> Windows

    source aiContext/bin/activate ---> Linux/Mac

2. Instalar dependencias

    pip install -r requirements.txt

3. Ejecutar

    uvicorn main:app --reload --port 8003

### 🐳 Ejecutar con Docker
#### Build

    docker build -t ai-service .

#### Run

    docker run -p 8003:8003 \
    -e GCS_BUCKET_NAME=... \
    -e OPENAI_API_KEY=... \
    -e PUBLIC_KEY_PATH=/app/secrets/bff_public.pem \
    -v ./secrets:/app/secrets \
    ai-service