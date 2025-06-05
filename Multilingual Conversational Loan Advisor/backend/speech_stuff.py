import requests
import io
import os
from pydub import AudioSegment

user_lang = ''

# Your API Key (Replace with your actual API key)
SARVAM_AI_API = "SARVAM API KEY"

# API endpoint for speech-to-text translation
API_URL = "https://api.sarvam.ai/speech-to-text-translate"

# Headers containing the API subscription key
HEADERS = {
    "api-subscription-key": SARVAM_AI_API
}

# Data payload for the translation request
DATA = {
    "model": "saaras:flash",
    "with_diarization": False
}

def split_audio(audio_path, chunk_duration_ms=5 * 60 * 1000):
    try:
        audio = AudioSegment.from_file(audio_path, format="mp3")  # Load MP3 file
        chunks = [audio[i:i + chunk_duration_ms] for i in range(0, len(audio), chunk_duration_ms)]
        return chunks
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return []

def translate_audio(audio_file_path, api_url = API_URL, headers = HEADERS, data = DATA):
    global user_lang
    chunks = split_audio(audio_file_path)
    if not chunks:
        return {"error": "Failed to process audio file."}

    responses = []
    for idx, chunk in enumerate(chunks):
        chunk_buffer = io.BytesIO()
        chunk.export(chunk_buffer, format="wav")  # Convert to WAV format
        chunk_buffer.seek(0)

        files = {'file': ('audiofile.wav', chunk_buffer, 'audio/wav')}

        try:
            response = requests.post(api_url, headers=headers, files=files, json=data)
            if response.status_code in [200, 201]:
                print(f"Chunk {idx} processed successfully.")
                transcript = response.json().get("transcript", "")
                user_lang = response.json().get('language_code')
                responses.append(transcript)
            else:
                print(f"Chunk {idx} failed. Status Code: {response.status_code}")
                print("Response:", response.text)
        except Exception as e:
            print(f"Error processing chunk {idx}: {e}")
        finally:
            chunk_buffer.close()

    collated_transcript = " ".join(responses)
    return {"transcript": collated_transcript, "lang_code" : user_lang}




