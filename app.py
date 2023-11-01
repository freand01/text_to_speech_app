from flask import Flask, request, Response
from gtts import gTTS
import io

app = Flask(__name__)

@app.route('/')
def index():
    return '<form method="POST" action="/convert"><input name="text"><button type="submit">Convert</button></form>'

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
    
    # Skapa en TTS från texten
    tts = gTTS(text)
    
    # Skapa en BytesIO buffer att spara mp3-filen i
    mp3_fp = io.BytesIO()
    tts.save(mp3_fp)
    mp3_fp.seek(0)
    
    return send_file(
        mp3_fp, 
        as_attachment=True, 
        download_name='speech.mp3', 
        mimetype='audio/mp3'
    )

if __name__ == '__main__':
    app.run(debug=True)
