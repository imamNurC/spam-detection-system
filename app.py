from flask import Flask, request, jsonify, render_template
import joblib
import os
from flask_cors import CORS

# Load the trained model and vectorizer
loaded_model = joblib.load('email_spam_model_indo.pkl')
vectorizer = joblib.load('vectorizer.pkl')

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
