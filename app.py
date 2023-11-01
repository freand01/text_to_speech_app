from flask import Flask, request, render_template, send_file
from bs4 import BeautifulSoup
from gtts import gTTS
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    doc_url = request.form['doc_url']
    text = get_text_from_doc(doc_url)
    
    if text:
        tts = gTTS(text=text, lang='sv')
        output_path = 'output.mp3'
        tts.save(output_path)
        
        return send_file(output_path, as_attachment=True)
    else:
        return "Kunde inte hämta eller konvertera texten."

def get_text_from_doc(published_doc_url):
    response = requests.get(published_doc_url)
    
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
    text = ' '.join([element.get_text() for element in text_elements])
    
    return text

if __name__ == '__main__':
    app.run(debug=True)
