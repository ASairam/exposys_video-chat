import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

load_dotenv()
twilio_account_sid ="ACf74cb93c1a5c7b87b50b25dd5e51bd9d"
twilio_api_key_sid ="SK28f440f29334e786382cb0a0bafaaca0"
twilio_api_key_secret ="lE0qBIrNxZ3DHLsnJ6FoQKZPFnaX5YDO"

app = Flask(__name__)




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.get_json(force=True).get('username')
    if not username:
        abort(401)

    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room='My Room'))

    return {'token': token.to_jwt().decode()}