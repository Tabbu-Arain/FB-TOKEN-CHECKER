from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Facebook App Credentials (Set in Render environment)
APP_ID = os.environ.get('FB_APP_ID')
APP_SECRET = os.environ.get('FB_APP_SECRET')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-token', methods=['POST'])
def handle_token():
    data = request.get_json()
    access_token = data.get('accessToken')

    if not access_token:
        return jsonify({'error': 'No access token provided'}), 400

    try:
        app_token = f"{APP_ID}|{APP_SECRET}"
        debug_url = f"https://graph.facebook.com/debug_token?input_token={access_token}&access_token={app_token}"
        debug_response = requests.get(debug_url).json()

        if 'error' in debug_response:
            return jsonify({'error': debug_response['error']['message']}), 400

        if not debug_response['data']['is_valid']:
            return jsonify({'error': 'Invalid access token'}), 401

        user_url = f"https://graph.facebook.com/me?fields=id,name,email,birthday,picture.width(200).height(200)&access_token={access_token}"
        user_response = requests.get(user_url).json()

        return jsonify({
            'id': user_response.get('id'),
            'name': user_response.get('name'),
            'email': user_response.get('email'),
            'birthday': user_response.get('birthday'),
            'picture': user_response.get('picture', {}).get('data', {})
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
