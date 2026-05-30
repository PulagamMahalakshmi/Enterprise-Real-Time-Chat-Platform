from flask_socketio import join_room, send
from datetime import datetime

from extensions import socketio
from database import messages_collection

online_users = {}

@socketio.on("join")
def handle_join(data):

    username = data["username"]
    room = data["room"]

    online_users[username] = room

    join_room(room)

    send(
        f"{username} joined the room",
        to=room
    )

    socketio.emit(
        "users",
        list(online_users.keys())
    )

@socketio.on("typing")
def typing(data):

    socketio.emit(
        "typing",
        data,
        to=data["room"]
    )

@socketio.on("message")
def handle_message(data):

    room = data["room"]
    msg = data["message"]
    username = data["username"]

    messages_collection.insert_one({
        "room": room,
        "sender": username,
        "message": msg,
        "timestamp": datetime.utcnow()
    })

    current_time = datetime.now().strftime("%I:%M %p")

    send(
        f"[{current_time}] {username}: {msg}",
        to=room
    )

@socketio.on("disconnect")
def handle_disconnect():

    socketio.emit(
        "users",
        list(online_users.keys())
    )