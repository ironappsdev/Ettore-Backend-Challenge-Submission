# Ettore Backend Challenge

Bienvenido a la prueba técnica de backend para **Ettore**, nuestra plataforma de salud digital. Este repositorio contiene un proyecto Django preconfigurado que deberás extender con nuevas funcionalidades, lógica asincrónica y una integración básica con modelos de lenguaje (LLMs). Consulta el **Enunciado que te enviamos** para conocer las tareas completas a desarrollar.

---

## ⚙️ Stack utilizado

- Python 3.10+
- Django 5+
- Django REST Framework
- Celery
- Redis (como broker de tareas)
- SQLite (base de datos local por simplicidad)

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

### 4. Crea el archivo `.env`

```bash
cp .env.example .env
```

Completa los valores necesarios, especialmente la clave API de tu proveedor LLM (OpenAI, Gemini, Together AI, etc.).

> ⚠️ Asegúrate de NO commitear este archivo.

### 5. Levanta Redis (si no lo tienes instalado)

```bash
docker run -d -p 6379:6379 redis
```

### 6. Ejecuta migraciones y datos de ejemplo

```bash
python manage.py migrate
python manage.py init_dummy_data
python manage.py createsuperuser  # (opcional, para acceder al admin)
```

### 7. Inicia el servidor y el worker de Celery

```bash
# Terminal 1
python manage.py runserver

# Terminal 2
celery -A backend worker --loglevel=info
```

---

## 🔍 Carpeta de pruebas

Este repositorio incluye ejemplos de pruebas para facilitar el desarrollo:

- `/httpie_examples.md`: comandos HTTPie listos para usar.
- `/test-clients/bruno/`: colección compatible con Bruno.
- `/test-clients/postman/`: colección exportable para Postman.

Puedes extenderlos con nuevos endpoints que desarrolles.

---

## 📁 Estructura relevante del repositorio

[Agrega aquí una breve descripción de las carpetas y archivos desarroolados.]

---

## 🛠 Consideraciones adicionales

- El sistema usa autenticación básica con `demo_user` / `demo1234`.
- Las rutas DRF básicas para usuarios, perfiles y mediciones ya están definidas.
- Debes agregar tu propia lógica para:
  - Tareas Celery.
  - Llamadas reales a un LLM.
  - Validación y persistencia de metas personalizadas.
  - Creación de notificaciones simuladas.

Consulta el **Enunciado que te enviamos** para los detalles sobre estas funcionalidades.

---

## 🧪 Entrega

- Comparte tu fork del repositorio con nosotros.
- Usa commits claros y descriptivos.
- Si agregas nuevas dependencias, actualiza `requirements.txt`:

```bash
pip freeze > requirements.txt
```

¡Buena suerte!
