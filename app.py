from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime
from pydub import AudioSegment
from google.cloud import speech
from google.cloud import language_v1
import json

app = Flask(__name__)

GOOGLE_CLOUD_CREDENTIALS = os.getenv("GOOGLE_CLOUD_CREDENTIALS")
if not GOOGLE_CLOUD_CREDENTIALS:
    GOOGLE_CLOUD_CREDENTIALS = input("Enter the path to your Google Cloud credentials JSON file: ")

if not os.path.exists(GOOGLE_CLOUD_CREDENTIALS):
    raise FileNotFoundError(f"Credentials file not found at {GOOGLE_CLOUD_CREDENTIALS}")

AudioSegment.converter = os.getenv("FFMPEG_PATH")
AudioSegment.ffprobe = os.getenv("FFPROBE_PATH")

DATA_FILE = "transcriptions.json"
transcriptions_by_date = {}

def load_transcriptions():
    global transcriptions_by_date
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            transcriptions_by_date = json.load(f)

def save_transcriptions():
    with open(DATA_FILE, "w") as f:
        json.dump(transcriptions_by_date, f, indent=4)

def reencode_audio(input_path, output_path, target_sample_rate=44100):
    """Re-encode the audio file to ensure compatibility."""
    try:
        audio = AudioSegment.from_file(input_path, format="webm")
        audio = audio.set_frame_rate(target_sample_rate)
        audio = audio.set_sample_width(2)
        audio.export(output_path, format="wav")
    except Exception as e:
        raise RuntimeError(f"Error re-encoding audio: {e}")

def transcribe_audio(file_path, sample_rate_hertz=44100):
    """Google Cloud Speech-to-Text for transcription."""
    client = speech.SpeechClient.from_service_account_json(GOOGLE_CLOUD_CREDENTIALS)
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript
    return ""

def analyze_emotion_with_nlp(text):
    """Google Cloud Natural Language API for emotion analysis."""
    client = language_v1.LanguageServiceClient.from_service_account_json(GOOGLE_CLOUD_CREDENTIALS)
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    sentiment = response.document_sentiment

    thresholds = {"happy": 0.25, "sad": -0.25, "angry_magnitude": 1.5}

    if sentiment.score > thresholds["happy"]:
        return "happy"
    elif sentiment.score < thresholds["sad"] and sentiment.magnitude > thresholds["angry_magnitude"]:
        return "angry"
    elif sentiment.score < thresholds["sad"]:
        return "sad"
    else:
        return "neutral"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/record", methods=["POST"])
def record():
    """Handle audio recording and process it."""
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]
    audio_path = "uploaded_audio.webm"
    audio_file.save(audio_path)

    if os.path.getsize(audio_path) == 0:
        return jsonify({"error": "Uploaded file is empty"}), 400

    try:
        resampled_path = "resampled_audio.wav"
        reencode_audio(audio_path, resampled_path)

        transcription = transcribe_audio(resampled_path)
        emotion = analyze_emotion_with_nlp(transcription)

        today = datetime.now().strftime('%Y-%m-%d')
        transcriptions_by_date[today] = {
            "transcription": transcription,
            "emotion": emotion
        }

        save_transcriptions()

        return jsonify({"transcription": transcription, "emotion": emotion, "success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/calendar-data", methods=["GET"])
def calendar_data():
    """Provide emotions data for the calendar."""
    return jsonify({date: data["emotion"] for date, data in transcriptions_by_date.items()}), 200

@app.route("/history", methods=["GET"])
def history():
    """Provide transcription history."""
    return jsonify(transcriptions_by_date), 200

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

@app.route("/history-page")
def history_page():
    return render_template("history.html")

if __name__ == "__main__":
    load_transcriptions()

    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)
