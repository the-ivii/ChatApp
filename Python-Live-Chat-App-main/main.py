from flask import Flask, render_template, request, session as flask_session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app, manage_session=False)  

rooms = {}

def generate_unique_code(length):
    while True:
        code = ''.join(random.choices(ascii_uppercase, k=length))
        if code not in rooms:
            break
    return code

@app.route("/", methods=["POST", "GET"])
def home():
    flask_session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = "join" in request.form
        create = "create" in request.form

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        room = code
        if create:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)

        flask_session["room"] = room
        flask_session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = flask_session.get("room")
    name = flask_session.get("name")
    if not room or not name or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("connect")
def handle_connect(auth):
    room = flask_session.get("room")
    name = flask_session.get("name")

    if not room or not name or room not in rooms:
        return False  # Reject the connection

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("message")
def handle_message(data):
    room = flask_session.get("room")
    name = flask_session.get("name")

    if room not in rooms:
        return

    content = {"name": name, "message": data["data"]}
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{name} said: {data['data']}")

@socketio.on("disconnect")
def handle_disconnect():
    room = flask_session.get("room")
    name = flask_session.get("name")

    if room in rooms:
        leave_room(room)
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
        else:
            send({"name": name, "message": "has left the room"}, to=room)
            print(f"{name} has left room {room}")

if __name__ == "__main__":
    socketio.run(app, debug=True)