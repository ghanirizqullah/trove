from flask import Flask, request, jsonify, render_template, send_file
from services import yt_search, yt_audio_download, get_dwarven_reaction, get_initial_reaction

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term')
    
    if not search_term:
        return jsonify({'error': 'Search term required'}), 400
    
    try:
        initial_reaction = get_initial_reaction(search_term)
        agent_reaction = get_dwarven_reaction(initial_reaction)
        results = yt_search(search_term)
        return jsonify({
            'initial_reaction': initial_reaction,
            'agent_reaction': agent_reaction,
            'results': results
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def download():
    url = request.form.get('url')
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    try:
        file_data, filename = yt_audio_download(url)
        
        if not file_data:
            return jsonify({'error': 'Download failed'}), 500
        
        # Send the in-memory file to the browser
        file_data.seek(0)  # Reset to beginning
        return send_file(
            file_data,
            mimetype='audio/mp4',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)