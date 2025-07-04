# Ettore Backend Challenge

Bienvenido/a a la prueba técnica de backend para **Ettore**, nuestra plataforma de salud digital. Este repositorio contiene un proyecto Django preconfigurado que deberás extender con nuevas funcionalidades, lógica asincrónica y una integración básica con modelos de lenguaje (LLMs).

---

## 🚀 Objetivo

Implementar un conjunto de funcionalidades que demuestren tus habilidades en modelado de datos, desarrollo de APIs REST, tareas asincrónicas con Celery y uso práctico de LLMs mediante API.

---

## ⚙️ Stack utilizado

- Python 3.10+
- Django 4+
- Django REST Framework
- Celery
- Redis (broker)
- SQLite (para facilitar la ejecución local)

---

## ▶️ Instrucciones para correr el entorno

### 1. Haz un fork del proyecto y clónalo

```bash
git clone https://github.com/[tu-usuario]/ettore-backend-challenge.git
cd ettore-backend-challenge
```

### 2. Crea y activa un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # o .\venv\Scripts\activate -- en Windows
```

### 3. Instala dependencias

```bash
pip install -r requirements.txt
```

### 4. Crea un archivo `.env`

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus claves personales, especialmente la clave de tu proveedor LLM.

> ⚠️ Asegúrate de no subir este archivo a tu repositorio.

### 5. Levanta Redis (si no lo tienes instalado)

```bash
docker run -d -p 6379:6379 redis
```

### 6. Ejecuta migraciones y servidor

```bash
# Aplica migraciones
python manage.py migrate

# Crea el superusuario
python manage.py createsuperuser

# Carga datos de ejemplo
python manage.py init_dummy_data

# Inicia el servidor
python manage.py runserver
```

### 7. Corre el worker de Celery (en otra terminal)

```bash
celery -A config worker --loglevel=info
```

---

## 🔐 Autenticación

La API usa autenticación con token. Puedes obtener un token vía:

```bash
POST /api/login/
```

Inclúyelo en los headers de tus requests:

```http
Authorization: Token tu_token_aquí
```

---

## 📚 Qué encontrarás en este repositorio

- App principal `core/` con modelos base `Usuario` y `Medicion`
- Carpeta `llm/` con función vacía `obtener_recomendacion()` que deberás implementar
- Carpeta `celery/` lista para definir tareas
- Modelo `NotificacionSimulada` para registrar alertas
- Archivo `.http` o `curl_examples.sh` con ejemplos de requests
- Archivo `.env.example` con las variables de entorno esperadas

---

## 🧪 ¿Qué debes desarrollar?

Consulta el documento `enunciado.pdf` o visita el link entregado con las instrucciones detalladas.

---

## 📩 Entrega

- Comparte tu fork del repositorio con nosotros
- Asegúrate de que el código esté bien documentado y siga las mejores prácticas
- Asegúrate de usar commits claros y mensajes descriptivos
- Asegúrate de definir tus librerías extras en `requirements.txt` con:

```bash
pip freeze > requirements.txt # En el directorio raíz del proyecto
# o Windows:
pip freeze | Out-File -Encoding UTF8 requirements.txt
```

---

## 🧪 Ejemplos de uso con `curl`

```bash
# Reemplaza con tu token real una vez obtenido
TOKEN="TU_TOKEN_AQUI"

# ✅ Login para obtener token (solo si no lo tienes aún)
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# ✅ Ingesta de una nueva medición
curl -X POST http://localhost:8000/api/mediciones/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{"tipo": "presion", "valor": 142}'

# ✅ Consulta de mediciones
curl -X GET http://localhost:8000/api/mediciones/ \
  -H "Authorization: Token $TOKEN"

# ✅ Consultar recomendaciones desde LLM
curl -X POST http://localhost:8000/api/recomendacion/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{"input": "¿Qué debería mejorar en mis hábitos?"}'

# ✅ Crear una meta personal (si implementado)
curl -X POST http://localhost:8000/api/metas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{"tipo": "pasos_diarios", "valor_objetivo": 8000}'
```

---

¡Gracias por participar en este desafío! 💙

Equipo Ettore
