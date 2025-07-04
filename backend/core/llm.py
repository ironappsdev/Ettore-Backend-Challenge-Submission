from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
from core.prompts import (SYSTEM_PROMPT_GENERATE_RECOMMENDATION,
                          USER_PROMPT_GENERATE_RECOMMENDATION
                        )
from core.models import Measurement, UserProfile

logger = logging.getLogger(__name__)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class OpenAIClient:
    def __init__(self, model: str = "gpt-4o-mini", test_mode: bool = False):
        self.model = model
        self.test_mode = test_mode
        if not test_mode:
            self.client = OpenAI(api_key=OPENAI_API_KEY)

    def obtener_recomendacion(self, user_profile: UserProfile, last_measurements: list[Measurement]):
        if self.test_mode:
            return "Esto es una recomendación de prueba"
        
        measurements_text = ""

        for measurement in last_measurements:
            measurements_text += f"Medición: {measurement.type} - {measurement.value} - {measurement.unit} - {measurement.recorded_at}\n"

        prompt = USER_PROMPT_GENERATE_RECOMMENDATION.format(
            user_gender=user_profile.gender,
            user_age=user_profile.age,
            user_weight_kg=user_profile.weight_kg,
            user_height_cm=user_profile.height_cm,
            user_chronic_conditions=user_profile.chronic_conditions,
            user_activity_level=user_profile.activity_level,
            last_measurements=measurements_text
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT_GENERATE_RECOMMENDATION},
                    {"role": "user", "content": prompt}
                ]
            )
        except Exception as e:
            return f"No te puedo ayudar en este momento. Intenta más tarde y recuerda siempre consultar con tu médico si es urgente :)"

        return response.choices[0].message.content
    

    def obtener_meta_personal(self):
        return "Esto es una meta personal de prueba"