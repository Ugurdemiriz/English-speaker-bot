---
title: English Speaker Bot
emoji: 💬
colorFrom: yellow
colorTo: purple
sdk: gradio
sdk_version: 5.0.1
app_file: app.py
pinned: false
license: apache-2.0
short_description: 'An English-speaking partner for language learners. '
---
# English Speaking Practice Bot 🎤🔊

An AI-powered English conversation bot using LangChain, Hugging Face, Gradio, Speech-to-Text, and Text-to-Speech.

## Features
- 🎤 Speak into your microphone
- 🤖 AI responds in English
- 🔊 Listen to the AI's spoken reply
- 📜 Conversation memory with LangChain

## Setup
1. Create a Hugging Face account and new Space (Gradio + Python 3.10).
2. Clone this repository.
3. Add your Hugging Face write token to GitHub:
   - Go to Settings → Secrets → Actions
   - Add a secret named `HF_TOKEN` with your Hugging Face token.

## Deploy
```bash
git add .
git commit -m "Initial English speaking bot"
git push origin main

An example chatbot using [Gradio](https://gradio.app), [`huggingface_hub`](https://huggingface.co/docs/huggingface_hub/v0.22.2/en/index), and the [Hugging Face Inference API](https://huggingface.co/docs/api-inference/index).