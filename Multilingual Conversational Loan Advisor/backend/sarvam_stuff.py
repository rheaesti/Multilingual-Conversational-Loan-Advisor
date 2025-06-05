from google.cloud import translate_v2 as translate
import requests
import json
import re


translate_client = translate.Client() 

temp = open("apis/api_keys.JSON")
api = json.load(temp)
sarvam_api = api["SARVAM_API"]
LANGUAGE_MAPPING = {
    "en": "en-IN", 
    "hi": "hi-IN",
    "bn": "bn-IN",
    "gu": "gu-IN", 
    "kn": "kn-IN", 
    "ml": "ml-IN", 
    "mr": "mr-IN", 
    "or": "od-IN", 
    "pa": "pa-IN", 
    "ta": "ta-IN", 
    "te": "te-IN"
}

def detect_lang(text):
    detected_lang = translate_client.detect_language(text)
    mapped_lang = LANGUAGE_MAPPING[detected_lang['language']]
    return mapped_lang

# Function to translate text
def translate_text(text, target_lang, source_lang):
    sentences = split_text(text) #spliting the text using regex
    final_response  = "" #the final response string
    url = "https://api.sarvam.ai/translate"
    print(f"translating from {source_lang} to {target_lang} ")
    headers = {
        'Content-Type': 'application/json',
        'API-Subscription-Key': sarvam_api 
    }

    for sent in sentences:
        payload = {
        "input": sent,
        "source_language_code": source_lang,
        "target_language_code": target_lang,
        "speaker_gender": "Female",
        "mode": "formal",
        "model": "mayura:v1",
        "enable_preprocessing": False,
        "output_script": "fully-native",
        "numerals_format": "international"
        }
        response = requests.post(url, json=payload, headers=headers)
        print("Translating...")
        response.raise_for_status() 
        final_response += response.json().get('translated_text', '')  
    return final_response
    
#splitting big text
def split_text(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return sentences
