import time
import json
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
    sid = request.sid

    if session.get("room") is not None:
        room = server.onlineRoom[session["room"]]
        user = server.onlineUser[sid]
        print("{} left the room {}".format(user.name, session["room"]))
        
        room.kick(sid)

        if room.getNumberOfUser() == 0:
            server.delRoom(session["room"])
            print("room {} is deleted".format(session["room"]))
    print("Player {} left the game".format(server.onlineUser[sid].name))
    server.delUser(sid)


@socketio.on("check_room_to_join")
def check_room(data):
    data = json.loads(data)
    global server
    room_id = data["room"]
    
    sid = request.sid

    server.onlineUser[sid].name = data["name"]
    server.onlineUser[sid].room_request = room_id

    if server.onlineRoom.get(room_id) is None:
        server.addRoom(server.onlineUser[sid])
        join_room(room_id)
        emit("room_status", {"status": "01"}, to=sid)
    # status_code:
        # 01: admin
        # 02: guest
        # 03: another player joivn
        # 00: full
    else:
        room = server.onlineRoom[room_id]
        flag = room.accept(server.onlineUser[sid])
        
        admin : User
        for key in room.userInRoom.keys():
            if room.userInRoom[key].uid != request.sid:
                admin = room.userInRoom[key]

        if flag is True:
            emit("room_status", {"status": "02", "name": admin.name}, to=sid)
            emit("room_status", {"status": "03", "name": server.onlineUser[request.sid].name}, to=admin.uid)
            
            join_room(room_id)
            
        else:
            emit("room_status", {"status": "00"}, to=sid)
            disconnect()
            print("room is full")
            return

    print("added {} to room {}\n".format(data["name"], room_id))
    session["name"] = data["name"]
    session["room"] = room_id


############### GAME PREPARATION ##################
@socketio.on("ready_to_start")
def readyToStart(msg):
    global server
    room = server.onlineRoom[session['room']]
    sid = request.sid

    if room.isRoomAvailable():
        emit("room_status", {"status": "need 2 players to play"}, to=sid)
        print("not enough player")
        return

    room.userInRoom[sid].isReady = True

    if not room.checkAllReady():
        emit("room_status", {"status": "waiting for another player"}, to=sid)
        print("not all ready")
        return
    room.startNewRound()
    room.startGame()
    emit("placeShip", to=session["room"])
    print("prepare for game")


@socketio.on("ready_to_start_bot")
def bot(msg):
    global server
    
    sid = request.sid
    room = server.onlineRoom[session['room']]

    if not room.isRoomAvailable():
        emit("room_status", {"status": "00"}, to=sid)       # 00: full
        return
    else:
        emit("room_status", {"status": "03", "name": "Miku Bot"}, to=sid)   
        #xác nhận add bot thành công và coi bot như opp của admin phòng
    room.startGame()
    emit("placeShip", to=session["room"])
    print("added bot to room")


@socketio.on("place_ship")
def placedShip(data):
    data = json.loads(data)
    global server
    sid = request.sid
    room = server.onlineRoom[session['room']].game

    if room.placeShip(data, sid):
        if len(room.players[sid].board.shipList) >= 5:
            room.players[sid].placedShip = True
        emit("room_status", {"status": "accepted"}, to=sid)
        print(room.players[sid].board)
    else:
        emit("room_status", {"status": "failed"}, to=sid)
    if room.checkAllReady():
        emit("start", to=session["room"])
        emit("turn", to=room.turn)
        print("playing game")


############ START GAME #############


@socketio.on("shoot")
def shoot(data):
    data = json.loads(data)
    global server

    room = server.onlineRoom[session['room']]

    cur = room.game.turn
    next = room.game.nextTurn()
    ally = room.game.players[cur]
    enemy = room.game.players[next]

    print("{} shot {}".format(ally, enemy))
    context: dict = ally.shoot(enemy, (data["x"], data["y"]))
    emit("update_context", {"context": context, "my_turn": True}, to=cur)
    emit("update_context", {"context": context, "my_turn": False}, to=next)

    if context["result"]:
        room.game.nextTurn()
        emit("turn", to=cur)

        if room.game.isCurrentPlayerWin(cur):
            emit("end_game", {"win": True}, to=cur)
            emit("end_game", {"win": False}, to=next)
    else:
        emit("turn", to=next)
    print("shoot successfully")


@socketio.on("shoot_bot")
def shoot_(data):
    data = json.loads(data)
    global server

    room = server.onlineRoom[session['room']]

    cur = room.game.turn
    ally = room.game.players[cur]
    bot: AIPlayer = room.game.players["bot"]
    
    print("{} shot {}".format(ally, bot))
    context: dict = ally.shoot(bot, (data["x"], data["y"]))
    emit("update_context", {"context": context, "my_turn": True}, to=cur)

    if context["result"]:
        if room.game.isCurrentPlayerWin(cur):
            emit("end_game", {"win": True}, to=cur)
            return

    else:
        # emit("update_context", {"context": context, "my_turn": False}, to=cur)
        print("bot ban \n")
        context: dict = bot.shoot(ally, bot.theBestAlgorithmInTheWorld())
        time.sleep(3)
        
        while context["result"]:
            emit("update_context", {"context": context, "my_turn": False}, to=cur)
            print("bot ban lien tuc \n")

            if room.game.isCurrentPlayerWin("bot"):
                emit("end_game", {"win": False}, to=cur)

            context: dict = bot.shoot(ally, bot.theBestAlgorithmInTheWorld())

        emit("update_context", {"context": context, "my_turn": False}, to=cur)
    emit("turn", to=cur)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
