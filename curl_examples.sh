#!/bin/bash

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
