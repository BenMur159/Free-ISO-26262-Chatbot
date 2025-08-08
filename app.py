from flask import Flask, render_template, request, jsonify
import webbrowser
import threading
from agent import Iso26262Chatbot

app = Flask(__name__)

iso26262Chatbot = Iso26262Chatbot()

@app.route("/")
def index():
    return render_template("iso26262Chatbot.html")

@app.route("/send", methods=["POST"])
def send():
    user_message = request.json.get("message")
    response = iso26262Chatbot.askIso26262Chatbot(user_message)
    return jsonify({"status": "success", "response": response})

def open_browser():
  webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
  threading.Timer(1.25, open_browser).start()  # Open browser shortly after server starts

  app.run(debug=False)
