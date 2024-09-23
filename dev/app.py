from oop import *
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, disconnect, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "lmao"
app.config["SESSION_TYPE"] = "filesystem"

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


@app.route("/")
def hello():
    return f"fun fact: if you are reading this, you are reading it from web browser"


server = Game()

# --- Connection and joining room---#


@socketio.event
@socketio.on('connect')
def connect():
    global server
    server.addUser(request.sid)
    print("user with id= {} has joined".format(request.sid))


# temp


@socketio.event
@socketio.on('disconnect')
def disconnect():
    global server

    if session["room"] is not None:
        user: User = server.onlineUser[request.sid]
        print("{} left the room {}".format(user.name, session["room"]))
        server.delUser(request.sid)
        server.onlineRoom[session["room"]].kick(request.sid)

        if (
            user.role == "admin"
            or server.onlineRoom[session["room"]].getNumberOfUser() == 0
        ):
            server.delRoom(session["room"])
            print("room {} is deleted".format(session["room"]))


@socketio.on("check-room-to-join")
def check_room(data):
    global server

    room_id = data["room"]

    server.onlineUser[request.sid].name = data["name"]
    server.onlineUser[request.sid].room_request = room_id

    if server.onlineRoom.get(room_id) is None:
        server.addRoom({"room_id": room_id, "name": data["name"], "uid": request.sid})
        join_room(room_id)
        emit("room-status", "accept", to=request.sid)
    else:
        flag = server.onlineRoom[room_id].accept(server.onlineUser[request.sid])
        if flag is True:
            emit("room-status", "accept", to=request.sid)
            join_room(room_id)
            print("added {} to room {}".format(data["name"], room_id))
        else:
            emit("room-status", "full", to=request.sid)
            disconnect()
            print("room is full")
            return

    print(server.onlineRoom[room_id])
    session["name"] = data["name"]
    session["room"] = room_id


# --- game preperation ---
@socketio.on("readyToStart")
def readyToStart(msg):
    global server
    idx = server.onlineRoom[session["room"]].getIndxInRoom(request.sid)

    emit("clientId", {"idx": idx}, to=request.sid)
    emit("placeShip", to=session["room"])


# temp


@socketio.on("placedShip")
def placedShip(data):
    global server
    server.onlineRoom[session["room"]].game.placedShip(data["idx"], data)

socketio.run(app, host='0.0.0.0', port=5000) 
