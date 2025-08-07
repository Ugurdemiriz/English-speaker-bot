import gradio as gr
import time
import json
import os
from datetime import datetime
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import tempfile
from gtts import gTTS
import speech_recognition as sr

# Log directory setup
os.makedirs("logs", exist_ok=True)

# Get Hugging Face API token from environment
api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not api_token:
    raise EnvironmentError("Missing HUGGINGFACEHUB_API_TOKEN in environment variables.")

# LLM configuration using HuggingFaceEndpoint
llm = HuggingFaceEndpoint(
    repo_id="tiiuae/falcon-7b-instruct",
    huggingfacehub_api_token=api_token,
    temperature=0.7,
    max_new_tokens=200
)

# LangChain memory for conversation context
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# Function to convert speech audio file to text
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return "Sorry, I couldn't understand."

# Function to log conversation and metrics
def log_interaction(user_text, response_text, latency_ms):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_input": user_text,
        "bot_response": response_text,
        "latency_ms": latency_ms
    }
    with open("logs/conversation_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

# Main chatbot logic with audio response
def chat_with_bot(audio_file):
    # 1. STT: Convert audio to text
    user_text = speech_to_text(audio_file)

    # 2. Start timer for response latency
    start_time = time.time()

    # 3. Get LLM response
    response_text = conversation.run(user_text)

    # 4. Measure latency
    latency_ms = round((time.time() - start_time) * 1000, 2)

    # 5. Convert response to speech
    tts = gTTS(response_text, lang="en")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)

    # 6. Log the interaction
    log_interaction(user_text, response_text, latency_ms)

    return user_text, response_text, temp_file.name

# Gradio UI definition
iface = gr.Interface(
    fn=chat_with_bot,
    inputs=gr.Audio(source="microphone", type="filepath"),
    outputs=[
        gr.Textbox(label="Your Speech (Recognized Text)"),
        gr.Textbox(label="Bot Response"),
        gr.Audio(label="Bot Voice", type="filepath")
    ],
    title="🗣️ English Speaking Practice Bot with LLMOps",
    description="Speak into the microphone and receive a spoken English reply. Logs interactions and monitors performance.",
)

iface.launch()

