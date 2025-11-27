import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from faster_whisper import WhisperModel

class STTService:
    def __init__(self, model_size="tiny", device="cpu", compute_type="int8"):
        print(f"Loading Whisper model: {model_size} on {device}...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print("Whisper model loaded.")

    def transcribe(self, audio_source):
        """
        Transcribes audio from a file path or a file-like object.
        """
        segments, info = self.model.transcribe(audio_source, beam_size=5)
        
        text = ""
        for segment in segments:
            text += segment.text + " "
        
        return text.strip()
