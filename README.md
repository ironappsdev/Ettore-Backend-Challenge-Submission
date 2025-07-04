# Ettore Backend Challenge Submission

Backend para la plataforma de salud digital Ettore. Permite gestionar usuarios, perfiles, mediciones, metas personalizadas y notificaciones simuladas, integrando recomendaciones de un modelo de lenguaje (LLM) y tareas asincrónicas.

---

## 🚀 Setup rápido

1. **Configura variables de entorno:**
   - Edita `.env` con tu `OPENAI_API_KEY` y configura Redis:
     - `CELERY_BROKER_URL=redis://localhost:6379/0`
     - `CELERY_RESULT_BACKEND=redis://localhost:6379/0`
2. **Levanta Redis:**
   ```bash
   docker run -d -p 6379:6379 redis
   ```
3. **Migraciones y datos demo:**
   ```bash
   python manage.py migrate
   python manage.py init_dummy_data
   ```
4. **Arranca el servidor y Celery:**
   ```bash
   # Terminal 1
   python manage.py runserver
   # Terminal 2
   celery -A backend worker --loglevel=info
   ```

---

## 🔑 Autenticación
- Usuario: `demo_user`
- Contraseña: `demo1234`

---

## 📚 Endpoints principales

- `/users/` - Usuarios
- `/profiles/` - Perfiles

- `/measurements/` - Mediciones
  - **GET**: Lista todas las mediciones registradas.
  - **POST**: Registra una nueva medición fisiológica. Dispara una tarea Celery que valida y guarda la medición. Si supera un threshold crítico, genera una notificación simulada y una recomendación personalizada usando el LLM. Responde 202 Accepted.

- `/recommendations/` - Recomendaciones LLM
  - **GET**: Lista las recomendaciones generadas para el usuario (puedes filtrar por `user_id`).
  - **POST**: Solicita la generación de una nueva recomendación personalizada. Dispara una tarea Celery que consulta las últimas mediciones y el perfil, llama al LLM y guarda la recomendación. Responde 202 Accepted.
    - **No requiere campos adicionales en el body.**

- `/goals/` - Metas personalizadas
  - **GET**: Lista las metas personalizadas creadas.
  - **POST**: Crea una nueva meta personalizada a partir de un input libre (`message`). Dispara una tarea Celery que consulta el perfil y mediciones, llama al LLM usando function calling y crea la meta. Responde 202 Accepted.
    - **Campo requerido:** `message` (texto libre describiendo la meta deseada).

Todos requieren autenticación básica.

---

## 🧪 Pruebas rápidas
- Usa los ejemplos en `api-tests/httpie_examples.sh`, `api-tests/bruno/` o `api-tests/postman/`.

---

## Notas
- No poseo formación médica. Los valores de threshold utilizados en este proyecto fueron generados por un LLM y tienen únicamente fines demostrativos para este ejercicio. No deben considerarse como referencias válidas para la práctica clínica ni para la toma de decisiones de salud.
