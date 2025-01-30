import os
import tempfile
from flask import Flask, request
from flask_cors import CORS
import whisper

app = Flask(__name__)
CORS(app)

model = "small.en"
audio_model = whisper.load_model(model)


@app.route("/transcribe", methods=["POST"])
def transcribe():
    if request.method == "POST":
        # Use small model and English language by default
        temp_dir = tempfile.mkdtemp()
        save_path = os.path.join(temp_dir, "temp.wav")

        wav_file = request.files["audio_data"]
        wav_file.save(save_path)

        result = audio_model.transcribe(save_path)
        return result["text"]
    else:
        return "This endpoint only processes POST wav blob"


if __name__ == "__main__":
    app.run(port=8000)
