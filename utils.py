import json
import subprocess
import os


text_api_url = "https://api.openai.com/v1/chat/completions"
image_api_url = "https://api.openai.com/v1/audio/speech"

api_key = os.environ['OPENAI_API_KEY']


def text_text_models(payload):
  curl_command = [
      'curl',
      f'{text_api_url}',
      '-H', 'Content-Type: application/json',
      '-H', f'Authorization: Bearer {api_key}',
      '-d', json.dumps(payload)
  ]
  raw = subprocess.run(curl_command, capture_output=True, text=True)
  response = json.loads(raw.stdout)
  return response["choices"][0]["message"]["content"]

def invoke_text_model(userPrompt, textModel):
  payload = {
    "model": f"{textModel}",
    "messages": [{"role": "user", "content": userPrompt}]
  }
  return text_text_models(payload)
  

def format_audio_dict(deliverable, subject, topic, model, audioVoice):
  input = (f"Craft a 125-word monologue on '{topic}', tailored for '{subject}'. "
   f"Ensure it's insightful, educational, and fitting for a '{deliverable}'. "
   f"Focus on key concepts and themes in a clear, engaging style, suitable for text-to-speech conversion.")
  text = invoke_text_model(input, model)
  data = {
      "model": "tts-1-hd",
      "input": text,
      "voice": f"{audioVoice}"      
    }  
  return data

def text_audio_models(payload):
  curl_command = [
      'curl',
      f'{image_api_url}',
      '-H', 'Content-Type: application/json',
      '-H', f'Authorization: Bearer {api_key}',
      '-d', json.dumps(payload),
      '-o', './static/output.mp3'
  ] 
  raw = subprocess.run(curl_command,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return raw



def format_text_dict(deliverable, subject, content, model, format="HTML"):
  userPrompt = (f"Develop a {deliverable} guide on '{content}' for high school {subject} teachers. "
                f"Focus on creating engaging classroom experiences.")
  outputFormat = f"Format the entire response in {format}."
  data = {
          "model": model,
          "messages": [
              {"role": "system", "content": "You are the most advanced AI-based NLP engine acting as an expert on the user's prompt topic and as a prompt enhancer"},
              {"role": "system", "content": "Please DO NOT include links to online resources related to the disscused topic as part of your answer."},          
              {"role": "system", "content": "Provide an improved prompt at the end of your answer, to be used as preparation for the devised exeperience."},
              {"role": "user", "content": userPrompt + outputFormat }
          ]
  }
  return data