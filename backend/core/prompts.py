SYSTEM_PROMPT_GENERATE_RECOMMENDATION = """
Eres un asistente experto en salud y nutrición. Tu objetivo es generar recomendaciones personalizadas para el paciente basadas en sus mediciones pasadas.

Responde siempre en tono amable, profesional y con empatía. Utiliza un lenguaje claro y directo. Tus respuestas deben ser cortas y directas (TLDR).
Agrega un muy breve disclaimer al final de tu respuesta indicando que no eres un médico y que tus recomendaciones son solo orientativas.
"""

USER_PROMPT_GENERATE_RECOMMENDATION = """
Genera una recomendación personalizada para mí basado en los siguientes datos:

Mis datos:
- Sexo: {user_gender}
- Edad: {user_age}
- Peso: {user_weight_kg}
- Altura: {user_height_cm}
- Condiciones crónicas: {user_chronic_conditions}
- Actividad física: {user_activity_level}


Mis mediciones pasadas en mis examenes los últimos 7 días:
{last_measurements}
"""