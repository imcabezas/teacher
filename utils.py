import subprocess
import json
import os


text_api_url = "https://api.openai.com/v1/chat/completions"
image_api_url = "https://api.openai.com/v1/audio/speech"

api_key = os.environ['OPENAI_API_KEY']


def text_text_models(payload):
  # Prepare the curl command
  curl_command = [
      'curl',
      f'{text_api_url}',
      '-H', 'Content-Type: application/json',
      '-H', f'Authorization: Bearer {api_key}',
      '-d', json.dumps(payload)
  ]
  # Execute the curl command
  raw = subprocess.run(curl_command, capture_output=True, text=True)
  response = json.loads(raw.stdout)
  # Return the output
  return response["choices"][0]["message"]["content"]

def invoke_text_model(userPrompt):
  payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": userPrompt}]
  }
  return text_text_models(payload)
  

def format_audio_dict(topic, audioVoice):
  input = f"Create an engaging monologue speaking on behalf of {topic}, limited to 125 words."
  input += f"Capture the essence of {topic} in a expressive manner, suitable for text-to-speech conversion."
  text = invoke_text_model(input)
  data = {
      "model": "tts-1-hd",
      "input": text,
      "voice": f"{audioVoice}"      
    }  
  return data

def text_audio_models(payload):
  # Prepare the curl command
  curl_command = [
      'curl',
      f'{image_api_url}',
      '-H', 'Content-Type: application/json',
      '-H', f'Authorization: Bearer {api_key}',
      '-d', json.dumps(payload),
      '-o', './static/output.mp3'
  ]
  # Execute the curl command
  raw = subprocess.run(curl_command,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  #response = json.loads(raw.stdout)
  # Return the output
  return raw




# Function to format the dictionary based on inputs
def format_text_dict(deliverable, subject, content, model, format="HTML"):
    userPrompt = f"Create a {deliverable} for high school teachers specializing in {subject}, focusing on the topic: '{content}'."
    userPrompt += " This deliverable should serve as a guide for designing engaging classroom experiences."
    outputFormat = f"Please format the 100% of your response as {format}."
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are the most advanced AI-based NLP engine acting as an expert on the user's prompt topic and as a prompt enhancer"},
            {"role": "system", "content": "Please DO NOT include links to online resources related to the disscused topic as part of your answer."},          
            {"role": "system", "content": "Provide an improved prompt at the end of your answer, to be used as preparation for the devised exeperience."},
            {"role": "user", "content": userPrompt},
            {"role": "user", "content": outputFormat}
        ]
    }
    return data