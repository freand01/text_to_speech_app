from flask import Flask, request, render_template, send_file, jsonify
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
        # Lägg till en timeout för att förhindra oändliga väntetider
        response = requests.get(doc_url, timeout=10)
        response.raise_for_status()  # Kontrollerar HTTP-fel som 4xx och 5xx
        
        text_to_convert = response.text
        
        tts = gTTS(text=text_to_convert, lang='sv')
        
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)  # write_to_fp istället för save för att skriva direkt till BytesIO
        mp3_fp.seek(0)
        
        return send_file(mp3_fp, as_attachment=True, download_name='output.mp3', mimetype='audio/mpeg')
    
    except requests.exceptions.Timeout:
        # Specifik hantering för en timeout
        return jsonify({"error": "Timeout vid hämtning av dokumentet"}), 408
    except requests.exceptions.HTTPError as http_err:
        # Specifik hantering för HTTP-fel
        return jsonify({"error": f"HTTP-fel uppstod: {http_err}"}), 500
    except requests.exceptions.RequestException as req_err:
        # Hantera andra requests-relaterade fel
        return jsonify({"error": f"Anslutningsfel uppstod: {req_err}"}), 500
    except Exception as e:
        # Generell felhantering för andra fel
        return jsonify({"error": f"Ett okänt fel inträffade: {str(e)}"}), 500

if __name__ == '__main__':
    # '0.0.0.0' gör din server tillgänglig på nätverket, ta bort under produktion om ej nödvändigt
    app.run(host='0.0.0.0', debug=False)
