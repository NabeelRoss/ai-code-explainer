from flask import Flask, request, jsonify, render_template
from model import CodeExplainer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize model once on startup
try:
    explainer = CodeExplainer()
except Exception as e:
    logger.error(f"CRITICAL: Model failed to load. Application may not work. Error: {e}")

# --- ROUTES ---

# Route to serve the frontend HTML dashboard
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint to handle code explanation requests
@app.route('/explain', methods=['POST'])
def explain_code():
    data = request.get_json()

    if not data or 'code' not in data:
        return jsonify({'error': 'No code provided in request body'}), 400

    code_snippet = data['code']
    
    # --- CHANGE 1: Increased max_len cap ---
    # We increased the default to 256 and the cap to 512
    # This allows the Flan-T5 model to write longer paragraphs.
    max_len = min(int(data.get('max_length', 256)), 512)

    if not code_snippet.strip():
        return jsonify({'error': 'Code snippet is empty. Please paste some code.'}), 400

    if len(code_snippet) > 2000:
         return jsonify({'error': 'Code snippet is too long. Keep it under 2000 characters.'}), 400

    try:
        explanation = explainer.explain(code_snippet, max_len)
        return jsonify({
            'success': True,
            'explanation': explanation
        })
    except Exception as e:
        logger.error(f"Error during request processing: {e}")
        return jsonify({'error': 'Internal server error processing request.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)