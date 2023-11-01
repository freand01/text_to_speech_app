from flask import Flask, request, render_template, send_file
from gtts import gTTS
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    doc_url = request.form['doc_url']
    
    try:
        # Hämta texten här (till exempel från ett Google-dokument eller någon annanstans)
        response = requests.get(doc_url)
        response.raise_for_status()
        
        # För detta exempel, antar vi att innehållet direkt är text
        # Du kan behöva anpassa detta beroende på hur du får texten
        text_to_convert = response.text
        
        # Konvertera texten till tal
        tts = gTTS(text=text_to_convert, lang='sv')
        
        # Spara tal som en bytes-ström snarare än en fysisk fil
        mp3_fp = BytesIO()
        tts.save(mp3_fp)
        mp3_fp.seek(0)
        
        return send_file(mp3_fp, as_attachment=True, download_name='output.mp3', mimetype='audio/mpeg')
    
    except Exception as e:
        return f"Ett fel inträffade: {e}"

if __name__ == '__main__':
    app.run(debug=True)
