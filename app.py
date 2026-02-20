from flask import  Flask, request, jsonify, render_template, send_file
from services import yt_search, yt_audio_download

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term')
    
    if not search_term:
        return jsonify({'error': 'Search term required'}), 400
    
    try:
        results = yt_search(search_term)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def download():
    url = request.form.get('url')
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    try:
        file_path = yt_audio_download(url)
        if not file_path or file_path == "":
            return jsonify({'error': 'Download failed - file not created'}), 500
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(debug=True)