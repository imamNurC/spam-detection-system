from flask import Flask, request, jsonify, render_template
import joblib

# Load the trained model and vectorizer
loaded_model = joblib.load('email_spam_model_indo.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Initialize the Flask app
app = Flask(__name__)

# Route to render the HTML page
@app.route('/')
def home():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)
