import os
import requests
import base64
import wave
from pydub import AudioSegment
import datetime

def generate_audio_filepath(text, session_id: str, lang):
    url = "https://api.sarvam.ai/text-to-speech"
    headers = {
        "api-subscription-key": "a2d6d5ce-0006-435d-a0a3-499930c87150",
        "Content-Type": "application/json"
    }
   
    output_dir = "generated_audio"
    os.makedirs(output_dir, exist_ok=True)
   
    # Add timestamp to create a unique filename for each request
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    
    def split_text(text, chunk_size=500):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
   
    sentences = split_text(text)
    temp_wav_files = []
   
    for i, chunk in enumerate(sentences):
        payload = {
            "inputs": [chunk],
            "target_language_code": lang,
            "speaker": "neel",
            "model": "bulbul:v1",
            "pitch": 0,
            "pace": 1.0,
            "loudness": 1.0,
            "enable_preprocessing": True,
        }
       
        response = requests.post(url, json=payload, headers=headers)
       
        if response.status_code == 200:
            audio = base64.b64decode(response.json()["audios"][0])
            temp_wav_file = os.path.join(output_dir, f"temp_chunk_{session_id}_{timestamp}_{i}.wav")
            temp_wav_files.append(temp_wav_file)
           
            with wave.open(temp_wav_file, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(22050)
                wav_file.writeframes(audio)
        else:
            print(f"Error generating audio for chunk {i}: {response.status_code}")
            return ""
   
    if temp_wav_files:
        combined_audio = AudioSegment.empty()
        for wav_file in temp_wav_files:
            audio_segment = AudioSegment.from_wav(wav_file)
            combined_audio += audio_segment
       
        # Use timestamp in the final filename to make it unique
        final_audio_filepath = os.path.join(output_dir, f"{session_id}_{timestamp}.webm")
       
        combined_audio.export(final_audio_filepath, format="webm")
       
        for temp_file in temp_wav_files:
            os.remove(temp_file)
       
        return final_audio_filepath
    else:
        print("No audio chunks were generated successfully")
        return ""