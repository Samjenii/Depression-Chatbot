import os
import google.generativeai as genai
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app)

# Configure the Google API key (environment variable)
os.environ['GOOGLE_API_KEY'] = 'AIzaSyDgTNcfDVLHBHWttnJEVC-hTHfBMt8rKvs'  # Replace with your own API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Initialize the generative model and chat
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gemini', methods=['POST'])
def gemini_response_chat():
    data = request.json
    app.logger.debug(f'Received data: {data}')

    try:
        query = data.get('query')
        response = chat.send_message(query)
        app.logger.debug(f'Response from chat: {response.text}')
        return jsonify({'response': response.text})
    except Exception as e:
        app.logger.error(f'Error processing request: {e}')
        return jsonify({'error': str(e)}), 500


# Remove or comment out the app.run() line for PythonAnywhere or Render deployment
if __name__ == "__main__":
    app.run(debug=True)
