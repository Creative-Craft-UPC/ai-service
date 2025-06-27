from typing import List, Optional
from pydantic import BaseModel, Field

class GPTExerciceRequest(BaseModel):
    prompt: str = Field(..., example="Genera una actividad de reconocimiento de emociones/actividad social.")

class GPTVoiceRequest(BaseModel):
    text: str = Field(..., example="¡Fui al parque, jugué mucho y me divertí!")
    voice: str = Field(default="nova", example="nova")
    audio_name: Optional[str] = Field(..., example="audio-alegría-9fdisa-38d8s9f8-s9a9f78s")
    instructions: str = Field(..., example="Lee el texto con una voz animada, brillante y rápida. Usa entonación ascendente y énfasis positivo")


class GPTResponse(BaseModel):
    id: str
    answer: str
