from flask import Flask, request, render_template, send_file
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    doc_url = request.form['doc_url']
    
    try:
        response = requests.get(doc_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Anta att vi vill extrahera all text från sidan, du kan anpassa detta baserat på dina behov
        text_to_convert = soup.get_text()
        
        tts = gTTS(text=text_to_convert, lang='sv')
        
        mp3_fp = BytesIO()
        tts.save(mp3_fp)
        mp3_fp.seek(0)
        
        return send_file(mp3_fp, as_attachment=True, download_name="output.mp3", mimetype='audio/mpeg')
    
    except Exception as e:
        return f"Ett fel inträffade: {e}"

if __name__ == '__main__':
    app.run(debug=True)
