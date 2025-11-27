import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from stt_service import STTService

# --- FastAPI App ---

app = FastAPI(title="Farmer AI STT API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
print("Initializing STT service...")
stt_service = STTService(model_size="tiny") 
print("STT service initialized.")

@app.get("/")
def read_root():
    return {"message": "Farmer AI STT API is running. Use /transcribe to convert speech to text."}

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Upload an audio file and get the transcription.
    """
    # Save to temp file to ensure compatibility with all ffmpeg formats
    suffix = f".{file.filename.split('.')[-1]}" if "." in file.filename else ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        shutil.copyfileobj(file.file, temp_audio)
        temp_path = temp_audio.name
    
    try:
        text = stt_service.transcribe(temp_path)
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
