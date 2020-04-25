import os

from flask import Flask, render_template, request, json
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


class Chatroom:
    users = []

    def __init__(self, name, text):
        self.name = name
        self.text = text

    def add(self, name):
        self.name = name

    def newmessage(self, msg):
        self.text += msg

    def adduser(self, username):
        self.users.append(username)

    def removeuser(self, username):
        self.users.remove(username)

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def serialize(self):
        data = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return data


chatrooms = [Chatroom("Default", "line0")]


def Serialize(chatrooms):
    data = json.dumps(chatrooms, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    return data


def Deserialize(data):
    global chatrooms
    chatrooms = Chatroom.from_json(json.loads(data))


@app.route("/")
def index():
    chatroomsJson = Serialize(chatrooms)
    print('root Route : ' + chatroomsJson)
    return render_template("index.html", chatroomsJson=chatroomsJson)


@app.route("/<string:name>")
def room(name):
    chatroom = next(filter(lambda x: x.name == name, chatrooms))
    if chatroom is not None:
        print('found chatroom ' + json.jsonify(chatroom))
        return json.jsonify(chatroom);


@socketio.on("send message")
def sendmessage(data):
    print('received message: ' + data["chatroom"])
    name = data["chatroom"]
    msg = data["message"]
    chatroom= next((x for x in chatrooms if x.name == name), None)
    if chatroom is not None:
        print('received message: found chatroom ' + data["message"])
        chatroom.newmessage(msg)
        emit("broadcast msg", {"text": chatroom.text}, broadcast=True)


@socketio.on("new chatroom")
def on_newchatroom(data):
    name = data["chatroom"]
    user = data["username"]
    chatroom = Chatroom(name, "")
    chatroom.adduser(user)
    chatrooms.append(chatroom)
    emit("broadcast chatroom", chatroom.serialize(), broadcast=True)


@socketio.on('join')
def on_join(data):
    name = data["room"]
    user = data["username"]
    chatroom = next(filter(lambda x: x.name == name, chatrooms))
    if chatroom is not None:
        chatroom.adduser(user)
        send(user + ' has entered the room.', chatrooms=Serialize(chatrooms))


@socketio.on('leave')
def on_leave(data):
    name = data["room"]
    user = data["username"]
    chatroom = next(filter(lambda x: x.name == name, chatrooms))
    if chatroom is not None:
        chatroom.removeuser(user)
        send(user + ' has exited the room.', chatrooms=Serialize(chatrooms))


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))


@socketio.on("my error event")
def on_my_event(data):
    raise RuntimeError()


@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])  # "my error event"
    print(request.event["args"])
