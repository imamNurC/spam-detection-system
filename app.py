from flask import Flask, request, jsonify, render_template
# import joblib
import os
from flask_cors import CORS
from moviepy.editor import VideoFileClip
import yt_dlp
import openai, whisper
openai.api_key = ""

# Load the trained model and vectorizer
# loaded_model = joblib.load('email_spam_model_indo.pkl')
# vectorizer = joblib.load('vectorizer.pkl')

# Initialize the Flask app
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
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
# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Get the email text from the request
#         data = request.get_json()
#         email_text = data['email']

#         # Transform the email text using the saved vectorizer
#         email_vector = vectorizer.transform([email_text])

#         # Make prediction using the loaded model
#         prediction = loaded_model.predict(email_vector)

#         # Return response based on prediction
#         if prediction[0] == "spam":
#             return jsonify({"result": "Pesan ini spam!"})
#         else:
#             return jsonify({"result": "Pesan Ini bukan spam"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400







#Load Whisper model sekali saja saat server dinyalakan
model = whisper.load_model("small")

def download_youtube_video(url, video_path='video.webm'):
    ydl_opts = {
        'format': 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best',
        'outtmpl': video_path,
        'quiet': True
    }
    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return video_path
    except Exception as e:
        print(f"Download error: {e}")
        return None

def extract_audio(video_path, audio_path='output.mp3'):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        video.close()
        return audio_path 
    except Exception as e:
        print(f"Audio extraction error: {e}")
        return None


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
#     return jsonify({"transcription": text})

###### TESTING ##########
# @app.route("/")
# def hello():
#     return "Whisper inference model is running on Colab with ngrok!"

@app.route('/process_video', methods=['POST'])
def process_video():
    input_type = request.form.get('input_type')
    youtube_url = request.form.get('url')
    mp4_url = request.form.get('mp4_url')
    file = request.files.get('file')

    video_path = None
    transcription = None
    error = None

    if input_type == 'youtube' and youtube_url:
        temp_video = os.path.join(UPLOAD_FOLDER, 'temp_youtube.webm')
        temp_audio = os.path.join(UPLOAD_FOLDER, 'temp_youtube.mp3')
        video_file = download_youtube_video(youtube_url, video_path=temp_video)

        if not video_file or not os.path.exists(video_file):
            error = "Gagal mengunduh video dari YouTube."
        else:
            audio_file = extract_audio(video_file, audio_path=temp_audio)
            if not audio_file or not os.path.exists(audio_file):
                error = "Gagal mengekstrak audio dari video."
            else:
                try:
                    result = model.transcribe(audio_file, language='id', verbose=False, fp16=False)
                    transcription = result["text"]
                    video_path = os.path.relpath(video_file, 'static')
                except Exception as e:
                    error = f"Transkripsi gagal: {str(e)}"

            # Clean up
            try:
                if os.path.exists(temp_audio): os.remove(temp_audio)
            except Exception as e:
                print(f"Cleanup error: {e}")

    elif input_type == 'mp4_url' and mp4_url:
        # Just simulate success for now
        transcription = f"Transkripsi hasil video dari URL MP4: {mp4_url}"

    elif input_type == 'upload' and file and file.filename.endswith('.mp4'):
        filename = file.filename
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        temp_audio = os.path.join(UPLOAD_FOLDER, f"{os.path.splitext(filename)[0]}.mp3")

        audio_file = extract_audio(save_path, audio_path=temp_audio)
        if not audio_file or not os.path.exists(audio_file):
            error = "Gagal mengekstrak audio dari video upload."
        else:
            try:
                result = model.transcribe(audio_file, language='id', verbose=False, fp16=False)
                transcription = result["text"]
                video_path = os.path.relpath(save_path, 'static')
            except Exception as e:
                error = f"Transkripsi gagal: {str(e)}"
        # Cleanup
        try:
            if os.path.exists(temp_audio): os.remove(temp_audio)
        except Exception as e:
            print(f"Cleanup error: {e}")
    else:
        error = "Input tidak valid, silakan coba lagi."

    return render_template('whisper.html', video_path=video_path, transcription=transcription, error=error)

if __name__ == '__main__':
    app.run(debug=True)
