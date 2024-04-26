import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask import request, jsonify
from .api import compare_message, paraphrase_by_avatar

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Flask app
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "default_secret")
CORS(app, resources={r"/compare_message": {"origins": "https://persuasivechatbotapp.onrender.com/"}})

# Define routes here, avoiding circular imports
@app.route('/compare_message', methods=['POST'])
def compare_message_endpoint():
    data = request.get_json()
    user_message = data['message']
    similar_text = compare_message(user_message)

    if similar_text:
        response = jsonify({'message': similar_text})
    else:
        response = jsonify({'message': 'No similar message found'})

    return response