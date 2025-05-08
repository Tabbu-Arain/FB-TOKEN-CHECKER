from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # <-- Add this
import requests
import os

app = Flask(__name__)
CORS(app)  # <-- Enable CORS

APP_ID = os.environ.get('FB_APP_ID')
APP_SECRET = os.environ.get('FB_APP_SECRET')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-token', methods=['POST'])
def handle_token():
    try:
        data = request.get_json()
        access_token = data.get('accessToken')

        if not access_token:
            return jsonify({'error': 'Token missing'}), 400

        # Validate token
        app_token = f"{APP_ID}|{APP_SECRET}"
        debug_url = f"https://graph.facebook.com/debug_token?input_token={access_token}&access_token={app_token}"
        debug_res = requests.get(debug_url).json()

        if 'error' in debug_res:
            return jsonify({'error': debug_res['error']['message']}), 400

        # Fetch user data
        user_url = f"https://graph.facebook.com/me?fields=id,name,email,birthday,picture&access_token={access_token}"
        user_res = requests.get(user_url).json()

        return jsonify({
            'id': user_res.get('id'),
            'name': user_res.get('name'),
            'email': user_res.get('email'),
            'birthday': user_res.get('birthday'),
            'picture': user_res.get('picture', {}).get('data', {})
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
