from flask import Flask, request, Response, render_template
from io import BytesIO
from gtts import gTTS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Antagande att du har en HTML-fil att rendera

@app.route('/convert', methods=['POST'])
def convert():
    doc_url = request.form['doc_url']
    
    try:
        # Hämta och konvertera text härifrån
        response = requests.get(doc_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        
        mp3_fp = BytesIO()
        tts = gTTS(text=text, lang='en')  # eller vilket språk du föredrar
        tts.save(mp3_fp)
        mp3_fp.seek(0)
        
        return send_file(
            mp3_fp,
            as_attachment=True,
            download_name='output.mp3',
            mimetype='audio/mpeg'
        )
    except Exception as e:
        return f"Ett fel inträffade: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
