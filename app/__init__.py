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
CORS(app, resources={r"/*": {"origins":"*"}}) # "https://persuasivechatbotapp.onrender.com"
# CORS(app, resources={r"/compare_message": {"origins": "https://persuasivechatbotapp.onrender.com/"}})

# Define routes here, avoiding circular imports
@app.route('/compare_message', methods=['POST'])
def compare_message_endpoint():
    try:
        data = request.get_json()  # Ensure JSON data is properly received
        if not data:
            print("invalid data passed!!")
            return jsonify({'error': 'Invalid data'}), 400  # Return proper status code for invalid data
        
        user_message = data.get('message')
        if not user_message:
            print("no message provided!!")
            return jsonify({'error': 'No message provided'}), 400  # Handle missing message
        
        similar_text = compare_message(user_message)
        response = jsonify({'message': similar_text if similar_text else 'No similar message found'})
    except Exception as e:
        print("error: ", str(e))
        return jsonify({'error': str(e)}), 500  # Handle unexpected errors
    
    return response
# def compare_message_endpoint():
#     data = request.get_json()
#     user_message = data['message']
#     similar_text = compare_message(user_message)

#     if similar_text:
#         response = jsonify({'message': similar_text})
#     else:
#         response = jsonify({'message': 'No similar message found'})

#     return response