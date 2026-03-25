from flask import Flask, request, jsonify, render_template, send_file, session
from services import yt_search, yt_audio_download, get_dwarven_reaction, get_initial_reaction
import json

app = Flask(__name__)
app.secret_key = 'dwarven_king_secret_treasure_vault_42'  # For session management

# Session state structure (stored in cookie, kept small):
# {
#   "conversation": [],  # List of {"role": "user"|"king", "content": "..."}
#   "current_query": "",
#   "current_results": [],  # Only essential fields (title, link, thumbnail, owner, duration, verification)
#   "current_page": 0,
#   "total_pages": 0,
#   "frustration_level": 1,
#   "interaction_count": 0
# }

def init_session():
    """Initialize session if not already done."""
    if 'conversation' not in session:
        session['conversation'] = []
        session['current_query'] = ''
        session['current_results'] = []
        session['current_page'] = 0
        session['total_pages'] = 0
        session['frustration_level'] = 1
        session['interaction_count'] = 0
        session.modified = True

def add_message(role: str, content: str):
    """Add a message to conversation history."""
    session['conversation'].append({
        'role': role,
        'content': content
    })
    session.modified = True

def calculate_frustration_level(interaction_count: int) -> int:
    """Calculate frustration based on how many interactions user has had."""
    if interaction_count <= 1:
        return 1  # First interaction: helpful
    elif interaction_count <= 3:
        return 2  # 2-3 interactions: mildly annoyed
    elif interaction_count <= 5:
        return 3  # 4-5 interactions: frustrated
    else:
        return 4  # 6+: exhausted, forcing recommendation

def slim_results(results):
    """Convert results to minimal form for session storage."""
    return [{
        'title': r.get('title', ''),
        'link': r.get('link', ''),
        'thumbnail': r.get('thumbnail', ''),
        'owner': r.get('owner', ''),
        'duration': r.get('duration', ''),
        'verification': r.get('verification', '')
    } for r in results]

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """Handle new search query with context awareness."""
    init_session()
    search_term = request.form.get('search_term')
    
    if not search_term:
        return jsonify({'error': 'Search term required'}), 400
    
    try:
        # Start new search (reset pagination, frustration, and conversation)
        session['current_query'] = search_term
        session['interaction_count'] = 1  # Reset to 1 for new search
        session['current_page'] = 0
        session['conversation'] = []  # Clear conversation history for fresh search
        session.modified = True
        
        # Add user message to history
        add_message('user', search_term)
        
        # Get initial reaction (quick response)
        initial_reaction = get_initial_reaction(search_term)
        
        # Search for results
        results = yt_search(search_term)
        session['current_results'] = slim_results(results)  # Store slim version
        session['total_pages'] = (len(results) + 2) // 3  # Calculate total pages (3 per page)
        session.modified = True
        
        # Calculate frustration level
        frustration_level = calculate_frustration_level(session['interaction_count'])
        session['frustration_level'] = frustration_level
        session.modified = True
        
        # Get context-aware dwarven reaction
        agent_reaction = get_dwarven_reaction(
            query=search_term,
            frustration_level=frustration_level,
            conversation_history=session.get('conversation', []),
            current_page=session['current_page'],
            total_pages=session['total_pages']
        )
        
        # Add king's response to history
        add_message('king', agent_reaction)
        
        return jsonify({
            'initial_reaction': initial_reaction,
            'agent_reaction': agent_reaction,
            'results': session['current_results'][:3],  # First 3 results
            'current_page': session['current_page'],
            'total_pages': session['total_pages'],
            'frustration_level': frustration_level,
            'interaction_count': session['interaction_count']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/next-page', methods=['POST'])
def next_page():
    """Load next 3 results (user clicked 'not quite')."""
    init_session()
    
    try:
        # Check if already at end (recommendation already made)
        if session['current_page'] >= session.get('total_pages', 0):
            return _make_recommendation()
        
        # Peek at what results would be on the next page
        next_page_num = session['current_page'] + 1
        start = next_page_num * 3
        end = start + 3
        
        # Get results from session
        next_results = session['current_results'][start:end]
        
        # If no results available for next page, trigger recommendation
        if not next_results:
            return _make_recommendation()
        
        # Results exist, so advance to next page
        session['current_page'] = next_page_num
        session.modified = True
        
        # User didn't pick - escalate frustration
        session['interaction_count'] += 1
        frustration_level = calculate_frustration_level(session['interaction_count'])
        session['frustration_level'] = frustration_level
        session.modified = True
        
        # King's reaction to "not quite"
        agent_reaction = get_dwarven_reaction(
            query=f"More options for '{session['current_query']}'",
            frustration_level=frustration_level,
            conversation_history=session.get('conversation', []),
            current_page=session['current_page'],
            total_pages=session['total_pages']
        )
        
        add_message('user', "Hmm, not quite...")
        add_message('king', agent_reaction)
        
        return jsonify({
            'agent_reaction': agent_reaction,
            'results': next_results,
            'current_page': session['current_page'],
            'total_pages': session['total_pages'],
            'frustration_level': frustration_level,
            'interaction_count': session['interaction_count']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prev-page', methods=['POST'])
def prev_page():
    """Go back to previous page."""
    init_session()
    
    try:
        if session['current_page'] <= 0:
            return jsonify({'error': 'Already at first page'}), 400
        
        session['current_page'] -= 1
        session.modified = True
        
        start = session['current_page'] * 3
        end = start + 3
        prev_results = session['current_results'][start:end]
        
        # King's reaction to "go back"
        agent_reaction = get_dwarven_reaction(
            query=f"Reconsidering options for '{session['current_query']}'",
            frustration_level=session['frustration_level'],
            conversation_history=session.get('conversation', []),
            current_page=session['current_page'],
            total_pages=session['total_pages']
        )
        
        add_message('user', "Actually, let me go back...")
        add_message('king', agent_reaction)
        
        return jsonify({
            'agent_reaction': agent_reaction,
            'results': prev_results,
            'current_page': session['current_page'],
            'total_pages': session['total_pages'],
            'frustration_level': session['frustration_level']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _make_recommendation():
    """King forces a recommendation on the indecisive user."""
    # Pick the first result as recommendation
    recommended = session['current_results'][0] if session['current_results'] else None
    
    if not recommended:
        return jsonify({'error': 'No results to recommend'}), 400
    
    recommendation_text = f"THAT'S ENOUGH! I'm recommending this beauty: {recommended.get('title', 'Unknown')} by {recommended.get('owner', 'Unknown')}. Take it or leave it, ye indecisive mortal!"
    
    add_message('user', "...")
    add_message('king', recommendation_text)
    
    # Mark as final by setting current_page to total_pages (indicating no more pages)
    session['current_page'] = session.get('total_pages', 0)
    session.modified = True
    
    return jsonify({
        'agent_reaction': recommendation_text,
        'results': [recommended],
        'recommended_result': recommended,
        'current_page': session['current_page'],
        'total_pages': session['total_pages'],
        'frustration_level': 4,
        'is_final_recommendation': True
    })

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