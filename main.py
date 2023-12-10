from flask import Flask, render_template, request
from utils import *



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Extract form data
    deliverable = request.form.get('deliverable')
    subject = request.form.get('subject')
    topic = request.form.get('topic')
    model = request.form.get('textModel') 
    audioVoice = request.form.get('audioVoice') 
  
    audioPrompt = format_audio_dict(deliverable, subject, topic, model, audioVoice)
    audioResponse = text_audio_models(audioPrompt)
  
    textPrompt = format_text_dict(deliverable, subject, topic, model, format="HTML")
    htmlContent = text_text_models(textPrompt)
    
    return render_template('result.html', topic=topic, htmlInfo=htmlContent, audioPrompt = audioPrompt["input"])


app.run(host='0.0.0.0', port=81)
