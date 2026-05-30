from flask import Flask, render_template, jsonify
import config

from extensions import bcrypt, jwt, socketio
from database import messages_collection

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY

bcrypt.init_app(app)
jwt.init_app(app)
socketio.init_app(app)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/messages/<room>")
def get_messages(room):

    messages = list(
        messages_collection.find(
            {"room": room},
            {"_id": 0}
        )
    )

    return jsonify(messages)

from routes.auth import auth_bp
app.register_blueprint(auth_bp)

import routes.chat

if __name__ == "__main__":
    socketio.run(app, debug=True)