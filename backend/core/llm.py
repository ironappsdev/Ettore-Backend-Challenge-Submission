from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
from core.prompts import (SYSTEM_PROMPT_GENERATE_RECOMMENDATION,
                          USER_PROMPT_GENERATE_RECOMMENDATION,
                          SYSTEM_PROMPT_GENERATE_GOAL,
                        )
from core.models import Measurement, UserProfile, Goal
import json
from dateutil.parser import parse as date_parse

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
    

    def obtener_meta_personal(self, user, user_input: str, user_profile: UserProfile, last_measurements: list[Measurement]):
        if self.test_mode:
            return "Esto es una meta personal de prueba"
        measurements_text = ""

        for measurement in last_measurements:
            measurements_text += f"Medición: {measurement.type} - {measurement.value} - {measurement.unit} - {measurement.recorded_at}\n"

        sys_prompt = SYSTEM_PROMPT_GENERATE_GOAL.format(
            user_gender=user_profile.gender,
            user_age=user_profile.age,
            user_weight_kg=user_profile.weight_kg,
            user_height_cm=user_profile.height_cm,
            user_chronic_conditions=user_profile.chronic_conditions,
            user_activity_level=user_profile.activity_level,
            last_measurements=measurements_text
        )

        functions = [
            {
                "name": "generate_goal",
                "description": "Crea una meta personal de salud para el paciente",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tipo_meta": {
                            "type": "string",
                            "enum": ["peso", "pasos", "presion", "glucosa", "agua", "sueño", "otro"],
                            "description": "Tipo de meta de salud"
                        },
                        "valor_objetivo": {
                            "type": "number",
                            "description": "Valor numérico objetivo"
                        },
                        "unidad": {
                            "type": "string",
                            "description": "Unidad de medida (kg, pasos, mmHg, mg/dL, litros, horas)"
                        },
                        "plazo": {
                            "type": "string",
                            "description": "Fecha de vencimiento de la meta en formato ISO (YYYY-MM-DD)'"
                        },
                        "descripcion": {
                            "type": "string",
                            "description": "Descripción detallada de la meta"
                        }
                    },
                    "required": ["tipo_meta", "valor_objetivo", "unidad", "descripcion"]
                }
            }
        ]

        logger.info(f"System prompt (LLM goal): {sys_prompt}")
        logger.info(f"User input (LLM goal): {user_input}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_input}
                ],
                functions=functions,
                function_call="auto"
            )

            logger.info(f"OpenAI raw response: {response}")

            message = response.choices[0].message
        
            if message.function_call:
                # Extraer los argumentos
                function_args = json.loads(message.function_call.arguments)
                
                plazo = function_args.get('plazo')
                expires_at = None
                if plazo:
                    try:
                        expires_at = date_parse(plazo)
                    except Exception:
                        pass
                
                # Crear la meta personal en la DB
                goal = Goal(
                    user=user,
                    user_input=user_input,
                    model_output=message.function_call.arguments,
                    target_value=function_args['valor_objetivo'],
                    target_unit=function_args['unidad'],
                    target_type=function_args['tipo_meta'],
                    target_description=function_args['descripcion'],
                    expires_at=expires_at,
                    model_name=self.model
                )
                goal.save()
                
                return {
                    "success": True,
                    "goal": goal,
                    "mensaje": f"Meta creada: {function_args['descripcion']}"
                }
            else:
                return {
                    "success": False,
                    "mensaje": "No se pudo crear la meta personal"
                }
        except Exception as e:
            logger.error(f"Error creating goal: {e}")
            return {
                "success": False,
                "mensaje": f"No te puedo ayudar en este momento. Intenta más tarde y recuerda siempre consultar con tu médico si es urgente :)"
            }