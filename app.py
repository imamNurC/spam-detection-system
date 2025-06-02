from flask import Flask, request, jsonify, render_template
# import joblib
import os
from flask_cors import CORS

# Load the trained model and vectorizer
# loaded_model = joblib.load('email_spam_model_indo.pkl')
# vectorizer = joblib.load('vectorizer.pkl')

# Initialize the Flask app
app = Flask(__name__)
UPLOAD_FOLDER = "static/downloads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CORS(app)  

# Route to render the HTML page
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/whisper', methods=['GET'])
def index():
    return render_template('whisper.html')

# @app.route('/process', methods=['POST'])
# def process():
#     url = request.form['url']
#     try:
#         yt = YouTube(url)
#         stream = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()
#         filename = f"{uuid.uuid4()}.mp4"
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         stream.download(output_path=UPLOAD_FOLDER, filename=filename)
#         # Transkripsi bisa dipanggil di sini
#         transcription = "Transkripsi dummy untuk contoh."
#         return render_template('index.html', video_path=f"downloads/{filename}", transcription=transcription)
#     except Exception as e:
#         return render_template('index.html', error=str(e))
     

# Route to handle the prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the email text from the request
        data = request.get_json()
        email_text = data['email']

        # Transform the email text using the saved vectorizer
        email_vector = vectorizer.transform([email_text])

        # Make prediction using the loaded model
        prediction = loaded_model.predict(email_vector)

        # Return response based on prediction
        if prediction[0] == "spam":
            return jsonify({"result": "Pesan ini spam!"})
        else:
            return jsonify({"result": "Pesan Ini bukan spam"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400



from flask import Flask, request, jsonify
# from moviepy.editor import VideoFileClip
# from flask_ngrok import run_with_ngrok
# import yt_dlp
# import openai, whisper
# openai.api_key = ""

# app = Flask(__name__)


# Load Whisper model sekali saja saat server dinyalakan
# model = whisper.load_model("small")

# def download_youtube_video(url, video_path='video.webm'):
#     ydl_opts = {
#         'format': 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best',
#         'outtmpl': video_path,
#         'quiet': True
#     }
#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])
#         return video_path
#     except Exception as e:
#         print(f"Download error: {e}")
#         return None

# def extract_audio(video_path, audio_path='output.mp3'):
#     try:
#         video = VideoFileClip(video_path)
#         audio = video.audio
#         audio.write_audiofile(audio_path)
#         video.close()
#         return audio_path
#     except Exception as e:
#         print(f"Audio extraction error: {e}")
#         return None


# @app.route('/transcribe', methods=['POST'])
# def transcribe():
#     url = request.json.get("youtube_url")
#     # url = 'https://www.youtube.com/watch?v=fwyV8c_2c6s'
#     if not url:
#         return jsonify({"error": "youtube_url is required"}), 400

#     # video_path = download_youtube_video('https://www.youtube.com/watch?v=fwyV8c_2c6s')
#     video_path = download_youtube_video(url)
#     if not video_path or not os.path.exists(video_path):
#         return jsonify({"error": "Failed to download video"}), 500

#     audio_path = extract_audio(video_path)
#     if not audio_path or not os.path.exists(audio_path):
#         return jsonify({"error": "Failed to extract audio"}), 500

#     try:
#         result = model.transcribe(audio_path, language='id', verbose=False, fp16=False)
#         text = result["text"]
#     except Exception as e:
#         return jsonify({"error": f"Transcription failed: {str(e)}"}), 500
#     finally:
#         try:
#             if os.path.exists(video_path): os.remove(video_path)
#             if os.path.exists(audio_path): os.remove(audio_path)
#         except Exception as e:
#             print(f"Cleanup error: {e}")

#     print(result)
    # return jsonify({"transcription": text})

###### TESTING ##########
# @app.route("/")
# def hello():
#     return "Whisper inference model is running on Colab with ngrok!"

@app.route('/process_video', methods=['POST'])
def process_video():
    # Ambil youtube_url dari body request (format JSON)
    youtube_url = request.json.get('youtube_url')

    # Cek apakah data youtube_url berhasil diterima
    if youtube_url is None:
        return jsonify({'error': 'youtube_url tidak ditemukan'}), 400

    # Log atau print untuk memverifikasi
    # print("Data yang diterima:", request.json)
    print("youtube_url:", youtube_url)         # Untuk melihat nilai youtube_url

    # Proses URL YouTube (contoh placeholder untuk proses lebih lanjut)
    transcription = process_youtube_video(youtube_url)

    return jsonify({'transcription': transcription})

def process_youtube_video(url):
    # Placeholder untuk logika pengunduhan, konversi, dan transkripsi

    return "Transkripsi hasil video dari: " + url


if __name__ == '__main__':
    app.run(debug=True)
