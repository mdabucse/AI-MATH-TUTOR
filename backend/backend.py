from model.youtube_transcriber import get_transcript_one,get_transcript_all
from model.chatbot import create_or_get_chat,fetch_all_chat_names,main,resume_chat_session
from flask_cors import CORS
from model.flowchart import flow_main
from model.video_to_transcribe import main_video
from flask import Flask, request, jsonify
import json

app = Flask(__name__)
CORS(app)
# Chatbot API Route
@app.route("/chat_create", methods=["POST"])
def chat_create():
    data = request.json
    chat_name = data.get("chat_name")
    response = create_or_get_chat(chat_name)
    if not chat_name:
        return jsonify({"error": "Missing chat_name or message"}), 400
    return jsonify({"response": response})

@app.route("/chat_resume", methods=["POST"])
def chat_resume():
    data = request.json
    chat_name = data.get("chat_name")
    response = resume_chat_session(chat_name)
    if not chat_name:
        return jsonify({"error": "Missing chat_name or message"}), 400
    return jsonify({"response": response})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    chat_name = data.get("chat_name")
    user_message = data.get("message")
    response = main(chat_name,user_message)
    if not chat_name or not user_message:
        return jsonify({"error": "Missing chat_name or message"}), 400
    return jsonify({"response": response})


# Chat History TODO: Working
@app.route("/chat_history", methods=["GET"])
def chat_history():
    chat_names = fetch_all_chat_names()
    return jsonify({"chat_names": chat_names})

# Flowchart API Route #TODO: Working
@app.route("/flowchart", methods=["POST"])
def flowchart():
    data = request.json
    text = data.get("text")
    
    if not text:
        return jsonify({"error": "Missing text input"}), 400
    
    mermaid_code = flow_main(text)
    return jsonify({"mermaid_code": mermaid_code})


# YouTube Transcript API Route #TODO: Working
@app.route("/transcript", methods=["POST"])
def transcript():
    data = request.json
    video_ids = data.get("video_ids")
    
    if not video_ids:
        return jsonify({"error": "Missing video_ids"}), 400
    if isinstance(video_ids, str):  # Single video case
        transcript = main_video(video_ids)
        return jsonify({"transcript": transcript})
    else:
        return jsonify({"error": "Invalid video_ids format"}), 400

@app.route("/load_transcribe", methods=["GET"])
def load_transcribe():
    with open(r"A:\Projects\Edu_Pro\backend\data\single.json",'r') as f:
        values = json.load(f)
    return jsonify({"message": values})

if __name__ == "__main__":
    app.run(debug=False)


"""
Main 
https://w4gw8kvg-5000.inc1.devtunnels.ms/

new_chat_creation(chat_name) -> POST
https://w4gw8kvg-5000.inc1.devtunnels.ms/chat_create

chat(message) -> POST
https://w4gw8kvg-5000.inc1.devtunnels.ms/chat

chat_history  -> GET
https://w4gw8kvg-5000.inc1.devtunnels.ms/chat_history

Chat history content
flow_chart(text)->POST
https://w4gw8kvg-5000.inc1.devtunnels.ms/flowchart

It returns mermaid code 
transcript(video_ids) -> POST
https://w4gw8kvg-5000.inc1.devtunnels.ms/transcript
it returns transcript of the video
"""
