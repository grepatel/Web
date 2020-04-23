import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

chatText = ""


@app.route("/")
def index():
    return render_template("index.html", chatText=chatText)


@socketio.on("send message")
def sendmessage(data):
    global chatText
    print('received json: ' + data["message"])
    chatText += data["message"]
    emit("broadcast", {"chatText": chatText}, broadcast=True)


@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
