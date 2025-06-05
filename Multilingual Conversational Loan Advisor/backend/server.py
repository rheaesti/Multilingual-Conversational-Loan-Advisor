import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import chatbot_utils
from chatbot_utils import sarvam_stuff
import speech_recognition as r
import datetime
import speech_stuff
import subprocess
import tts
import time

main_lang = 'en-IN'
user_lang : str

UPLOAD_FOLDER = 'audio_uploads'
GENERATED_AUDIO_FOLDER = 'generated_audio'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app)  #cross origin something lets frontend get to the backend

@app.route('/chat', methods=['POST'])
def chat():

    data = request.json
    print(data)
    user_message = data.get("message")
    session_id = data.get("name")
    print(user_message, session_id)

    user_lang = sarvam_stuff.detect_lang(user_message) #getting the user language
    print(user_lang)
    if user_lang != "en-IN":
        text_to_send = sarvam_stuff.translate_text(user_message, main_lang, user_lang) #translating the language to english
        bot_response = chatbot_utils.get_response(session_id, text_to_send)
        final_response = sarvam_stuff.translate_text(bot_response, user_lang, main_lang)
    else:
        bot_response = chatbot_utils.get_response(session_id, user_message)
        final_response = bot_response

    return jsonify({"response": final_response})

@app.route('/process-audio', methods=['POST'])
def speech_to_text_to_speech():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    session_id = request.form.get('userId', 'anonymous')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    webm_filename = f"{session_id}_{timestamp}.webm"
    mp3_filename = f"{session_id}_{timestamp}.mp3"
   
    webm_filepath = os.path.join(UPLOAD_FOLDER, webm_filename)
    mp3_filepath = os.path.join(UPLOAD_FOLDER, mp3_filename)
    audio_file.save(webm_filepath)
    
    # Convert WebM to MP3 using ffmpeg
    try:
        subprocess.run(["ffmpeg", "-i", webm_filepath, "-q:a", "2", "-acodec", "libmp3lame", mp3_filepath], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Audio conversion failed: {str(e)}"}), 500
    
    # Process audio to text
    transcription = speech_stuff.translate_audio(mp3_filepath)
    user_message = transcription["transcript"]
    user_lang = transcription["lang_code"]
    
    # Get chatbot response
    if user_lang == "en-IN":
        bot_response = chatbot_utils.get_response(session_id, user_message)
        final_response = bot_response
    else:
        bot_response = chatbot_utils.get_response(session_id, user_message)
        final_response = sarvam_stuff.translate_text(bot_response, user_lang, main_lang)
   
    # Generate audio response
    audio_filepath = tts.generate_audio_filepath(final_response, session_id, user_lang)
    audio_filename = os.path.basename(audio_filepath)
    print(f"Generated audio file: {audio_filepath}")

    time.sleep(2)

    return jsonify({
        "success": True,
        "transcription": transcription,
        "response": final_response,
        "audio_url": f"/generated_audio/{audio_filename}"
    })

@app.route('/generated_audio/<filename>', methods=['GET'])
def serve_audio(filename):
    # Make sure to serve from the correct directory
    if not os.path.exists(os.path.join(GENERATED_AUDIO_FOLDER, filename)):
        return jsonify({"error": "Audio file not found"}), 404
    return send_from_directory(GENERATED_AUDIO_FOLDER, filename)

@app.route('/uploads/<filename>', methods=['GET'])
def serve_uploads(filename):
    # For serving uploaded audio files if needed
    if not os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
        return jsonify({"error": "Uploaded file not found"}), 404
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/submit-loan', methods=['POST', 'GET'])
def sleep():
    loan_data = request.json
    session_id = loan_data["userId"]
    chatbot_utils.put_in_db(session_id, loan_data)

    print(loan_data)
    return jsonify({
            "success": True,
            "message": "Loan application received successfully",
            "loan_id": loan_data['Loan_ID']
        }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)