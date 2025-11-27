import sounddevice as sd
import scipy.io.wavfile as wav
import requests
import tempfile
import os
import sys

# Configuration
API_URL = "http://localhost:8000/transcribe"
SAMPLE_RATE = 44100  # Hertz
DURATION = 5  # Seconds to record

def record_audio(duration, fs):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    return recording

def save_and_send(recording, fs):
    # Save to a temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        wav.write(temp_wav.name, fs, recording)
        temp_path = temp_wav.name

    try:
        print(f"Sending audio to {API_URL}...")
        with open(temp_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(API_URL, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("\n--- Transcription ---")
            print(result.get("text", "No text found"))
            print("---------------------")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Failed to send audio: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    print("Farmer AI Voice Client")
    print("1. Record 5 seconds")
    print("2. Exit")
    
    while True:
        choice = input("\nEnter choice (1/2): ")
        if choice == '1':
            audio_data = record_audio(DURATION, SAMPLE_RATE)
            save_and_send(audio_data, SAMPLE_RATE)
        elif choice == '2':
            break
        else:
            print("Invalid choice")
