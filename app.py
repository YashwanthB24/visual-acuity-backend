import os
import tempfile
from flask import Flask, request
from flask_cors import CORS
import whisper

app = Flask(__name__)
CORS(app)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if request.method == "POST":
        # Use small model and English language by default
        model = "tiny.en"
        audio_model = whisper.load_model(model)

        temp_dir = tempfile.mkdtemp()
        save_path = os.path.join(temp_dir, "temp.wav")

        wav_file = request.files["audio_data"]
        wav_file.save(save_path)

        result = audio_model.transcribe(save_path)
        return result["text"]
    else:
        return "This endpoint only processes POST wav blob"


# No changes needed here for Gunicorn; app is callable by default.



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Get the assigned port
    print(f"Starting server on port {port}")  # Optional for debugging
    app.run(host="0.0.0.0", port=port)  # Bind to all network interfaces