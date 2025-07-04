# ==============================
# BASE TEST – endpoints prehechos
# ==============================

# Usuario de prueba:
#   username: demo_user
#   password: demo1234

# Listar usuarios
http -a demo_user:demo1234 GET http://localhost:8000/api/users/

# Listar perfiles
http -a demo_user:demo1234 GET http://localhost:8000/api/profiles/

# Listar mediciones
http -a demo_user:demo1234 GET http://localhost:8000/api/measurements/


# ==============================
# EVALUATION TEST – endpoints a implementar
# ==============================

# Crear nueva medición
http -a demo_user:demo1234 POST http://localhost:8000/api/measurements/ \
  user=1 \
  type="bp_sys" \
  value:=150 \
  unit="mmHg" \
  recorded_at="2025-07-01T10:00:00Z"

# Llamada al endpoint de recomendación LLM (a implementar)
http -a demo_user:demo1234 POST http://localhost:8000/api/recommendation/ \
  user_id:=1

# (Opcional) Prompt con function calling para crear meta personalizada
http -a demo_user:demo1234 POST http://localhost:8000/api/llm-function/ \
  message="Quiero bajar de peso y caminar 40 minutos todos los días"

