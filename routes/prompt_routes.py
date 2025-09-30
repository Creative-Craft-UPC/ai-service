import base64
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import requests
from models.schemas import GPTExerciseRequest, GPTVoiceRequest
from config.openai_config import text_client, speech_client
import io
from openai.helpers import LocalAudioPlayer
from fastapi.responses import FileResponse

from services.storage_service import upload_audio_to_gcs

router = APIRouter()


@router.post("/exercise/")
async def gpt_generate_exercise(exercise_prompt: GPTExerciseRequest):
    try:
        response = text_client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:creativecraft:asd-activities-v5:Bmov5us8",
            messages=[{"role": "user", "content": [
                {
                    "type": "text",
                    "text": exercise_prompt.prompt
                }
                ]}],
            temperature=1.0,
            max_tokens=2048,
            top_p=1.00
        )
        return{"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/audio/download")
async def gpt_generate_audio(audio_prompt: GPTVoiceRequest):
    audio_filename = f"{audio_prompt.audio_name}.mp3"
    custom_directory = Path(__file__).parent/ "audios"
    custom_directory.mkdir(parents=True, exist_ok=True)
    speech_file_path = custom_directory / audio_filename
    async with speech_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=audio_prompt.text,
        instructions=audio_prompt.instructions,
        response_format="mp3"
    ) as response:
           await response.stream_to_file(speech_file_path)
    bucket_name = "socialfun-audios"
    public_url = upload_audio_to_gcs(
        local_file_path=str(speech_file_path),
        bucket_name=bucket_name,
        destination_blob_name=f"audios/{audio_filename}"
    )

    return JSONResponse(content={"audio_url": public_url})
    #return FileResponse(
    #     speech_file_path,
    #     media_type="audio/wav",
    #     filename=audio_filename
    #)

@router.post("/audio/real-time")
async def gpt_generate_audio(audio_prompt: GPTVoiceRequest):
    async with speech_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=audio_prompt.text,
        instructions=audio_prompt.instructions,
        response_format="pcm"
    ) as response:
           await LocalAudioPlayer().play(response)
 


#@router.post("gpt/image")
#async def gpt_generate_emotion(data_emotion: GPTEmotionRequest):
#    try:
#        response = requests.get(data_emotion.image)
#        if response.status_code == 200:
#            base64_image = base64.b64encode(response.content).decode("utf-8")
#        else:
#            raise Exception(f"Error al descargar imagen: {response.status_code}")
#    
#        
#        response = client.chat.completions.create(
#            model="gpt-4o-mini",
#            messages=[{"role": "user", "content": [
#                {
#                    "type": "text",
#                    "text": data_story.text
#                },
#                {
#                    "type": "image_url",
#                    "image_url": {
#                            "url": f"data:image/jpg;base64, {base64_image}"
#                        }
#                }
#                ]}],
#            temperature=0.7
#        )
#        return{"response": response.choices[0].message.content}
#    except Exception as e:
#        raise HTTPException(status_code=500, detail=str(e))
#    
#@router.post("/gpt/voice")
#async def gpt_generate_audio(data_audio: GPTRequest):
#    try:
#        # Primero generamos texto con GPT
#        response = client.chat.completions.create(
#            model="gpt-4o-mini",
#            messages=[{"role": "user", "content": data.prompt}]
#        )
#        text_output = response.choices[0].message.content
#
#        # Luego generamos audio con TTS
#        audio_response = client.audio.speech.create(
#            model="gpt-4o-mini-tts", 
#            voice=data.voice,
#            input=text_output,
#            temperature=0.7
#        )
#
#        audio_bytes = io.BytesIO()
#        audio_response.stream_to_file(audio_bytes)
#        audio_bytes.seek(0)
#
#        return StreamingResponse(audio_bytes, media_type="audio/mpeg")
#    except Exception as e:
#        raise HTTPException(status_code=500, detail=str(e))
#    
#
