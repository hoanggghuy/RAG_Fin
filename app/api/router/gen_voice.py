from gen_voice.Whisper import Generate_Voice
from fastapi import APIRouter

router_genvoice = APIRouter(
    prefix="/gen-voice",
    tags=["gen-voice"]
)

@router_genvoice.post("/gen-voice")
async def gen_voice():
    generate_voice = Generate_Voice(filename="test.wav",duration=3,sample_rate=16000)
    transcript = generate_voice.gen_text_from_audio()
    return {f"You said": transcript}
