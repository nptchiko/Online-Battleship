from oop import *
from flask import Flask, session, request
from flask_socketio import SocketIO, emit, join_room, disconnect

app = Flask(__name__)
app.config["SECRET_KEY"] = "lmao"
app.config["SESSION_TYPE"] = "filesystem"

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


@app.route("/")
def hello():
    return f"fun fact: if you are reading this, you are reading it from web browser"


server = Server()


################ CONNECTION ANF JOINING ROOM ####################


@socketio.on("connect")
def connect():
    global server

    server.addUser(request.sid)
    print("user with id = {} has joined".format(request.sid))


@socketio.on("disconnect")
def disconnect():
    global server

    if session.get("room") is not None:
        user: User = server.onlineUser[request.sid]
        print("{} left the room {}".format(user.name, session["room"]))
        server.delUser(request.sid)
        server.onlineRoom[session["room"]].kick(request.sid)

        if server.onlineRoom[session["room"]].getNumberOfUser() == 0:
            server.delRoom(session["room"])
            print("room {} is deleted".format(session["room"]))


@socketio.on("check-room-to-join")
def check_room(data):
    global server

    room_id = data["room"]

    server.onlineUser[request.sid].name = data["name"]
    server.onlineUser[request.sid].room_request = room_id

    if server.onlineRoom.get(room_id) is None:
        server.addRoom(server.onlineUser[request.sid])
        join_room(room_id)
        emit("room_status", {"status": "accept"}, to=request.sid)

    else:
        flag = server.onlineRoom[room_id].accept(server.onlineUser[request.sid])
        if flag is True:
            emit("room_status", {"status": "accept"}, to=request.sid)
            join_room(room_id)
            print("added {} to room {}".format(data["name"], room_id))
        else:
            emit("room_status", {"status": "full"}, to=request.sid)
            disconnect()
            print("room is full")
            return

    print(server.onlineRoom[room_id])
    session["name"] = data["name"]
    session["room"] = room_id


############### GAME PREPARATION ##################
@socketio.on("readyToStart")
def readyToStart(msg):
    global server

    if server.onlineRoom[session["room"]].isRoomAvailable():
        emit("room_status", {"status": "need 2 players to play"}, to=request.sid)
        print("not enough player")
        return

    server.onlineRoom[session["room"]].userInRoom[request.sid].isReady = True

    if not server.onlineRoom[session["room"]].checkAllReady():
        emit("room_status", {"status": "waiting for another player"}, to=request.sid)
        print("not all ready")
        return
    server.onlineRoom[session["room"]].startGame()
    emit("placeShip", to=session["room"])
    print("prepare for game")


@socketio.on("play_with_bot")
def bot(msg):
    global server
    if not server.onlineRoom[session["room"]].isRoomAvailable():
        emit("room_status", {"status": "full"}, to=request.sid)
        return
    server.onlineRoom[session["room"]].startGame()
    emit("placeShip", to=session["room"])
    print("added bot to room")


@socketio.on("placeShip")
def placedShip(data):
    global server

    if server.onlineRoom[session["room"]].game.placeShip(data, request.sid):
        server.onlineRoom[session["room"]].game.players[request.sid].placedShip = True
        emit("room_status", {"status": "accepted"}, to=request.sid)
    else:
        emit("room_status", {"status": "failed"}, to=request.sid)
    if server.onlineRoom[session["room"]].game.checkAllReady():
        emit("start", to=session["room"])
        emit("turn", to=server.onlineRoom["session"].game.turn)
        print("playing game")


############ START GAME #############


@socketio.on("shoot")
def shoot(data):
    global server
    cur = server.onlineRoom[session["room"]].game.turn
    next = server.onlineRoom[session["room"]].game.nextTurn()
    ally = server.onlineRoom[session["room"]].game.players[cur]
    enemy = server.onlineRoom[session["room"]].game.players[next]

    context: dict = ally.shoot(enemy, data["coord"])
    emit("update_context", {"context": context, "my_turn": True}, to=cur)
    emit("update_context", {"context": context, "my_turn": False}, to=next)

    if context["result"]:
        server.onlineRoom[session["room"]].game.nextTurn()
        if cur == "bot":
            shoot(ally.shoot(enemy, ally.theBestAlgorithmInTheWorld()))
        else:
            emit("turn", to=cur)
    else:
        if next == "bot":
            shoot(enemy.shoot(ally, enemy.theBestAlgorithmInTheWorld()))
        else:
            emit("turn", to=next)
    print("shoot successfully")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
