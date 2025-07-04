from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
from core.prompts import SYSTEM_PROMPT_GENERATE_RECOMMENDATION
from core.models import Measurement

logger = logging.getLogger(__name__)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class OpenAIClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        # self.client = OpenAI(api_key=OPENAI_API_KEY)

    def obtener_recomendacion(self, last_measurements: list[Measurement]):
        for measurement in last_measurements:
            logger.info(f"Measurement: {measurement.type} - {measurement.value} - {measurement.unit} - {measurement.recorded_at}")
        #TODO: Build the prompt and call the llm
        return "Esto es una recomendación de prueba"
    

    def obtener_meta_personal(self):
        return "Esto es una meta personal de prueba"