from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import request, abort
from flask_socketio import SocketIO,send
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

load_dotenv()
twilio_account_sid = "ACf74cb93c1a5c7b87b50b25dd5e51bd9d"
twilio_api_key_sid = "SK28f440f29334e786382cb0a0bafaaca0"
twilio_api_key_secret = "lE0qBIrNxZ3DHLsnJ6FoQKZPFnaX5YDO"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


@app.route('/login', methods=['POST'])
def login():
    username = request.get_json(force=True).get('username')
    if not username:
        abort(401)

    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room='My Room'))
    socketio.run(app,port=6203)
    return {'token': token.to_jwt().decode()}
