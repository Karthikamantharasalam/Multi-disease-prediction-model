# -*- coding: utf-8 -*-
"""MULTI DISEASE PREDICT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1paP7GxXqAbzqCtlw42Vub4T3AbmuGog4
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install Flask pyngrok scikit-learn pandas matplotlib seaborn colorama
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from flask import Flask, render_template, request, redirect, url_for
from pyngrok import ngrok
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import classification_report
!pip install colorama
import colorama
from colorama import Back
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

!ngrok config add-authtoken "your auth token"

from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename
import os
import numpy as np
import pandas as pd
import cv2
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from pyngrok import ngrok
from flask import Flask, request, render_template_string
from pyngrok import ngrok
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}



# Load Pneumonia model
pneumonia_model = load_model('/content/drive/MyDrive/dataset/pneumoniapredictionmodel.keras')

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def predict_pneumonia(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (150, 150))
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    prediction = pneumonia_model.predict(img)
    filename = os.path.basename(image_path)
    if prediction > 0.7:
      return 'Pneumonia', filename
    else:
      return 'Normal', filename

# Load the dataset
dataset = pd.read_csv("/content/drive/MyDrive/heart /heart (2).csv")

# Preprocess data
predictors = dataset.drop("target", axis=1)
target = dataset["target"]

# Split the dataset into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(predictors, target, test_size=0.2, random_state=0)

# Train RandomForest model
rf = RandomForestClassifier(random_state=0)
rf.fit(X_train, Y_train)

# Function to give advice and explanation
def get_advice_and_explanation(input_data):
    explanation = []
    advice = []

    # Age advice
    if input_data[0] > 50:
        explanation.append("Age is a risk factor (Age > 50).")
        advice.append("Maintain regular checkups and a healthy lifestyle to reduce age-related risks.")

    # Cholesterol advice
    if input_data[4] > 200:
        explanation.append("High cholesterol (Cholesterol > 200 mg/dl) is a risk factor.")
        advice.append("Adopt a low-fat diet and exercise to lower cholesterol levels.")

    # Chest pain type advice
    if input_data[2] == 4:
        explanation.append("Asymptomatic chest pain is a potential sign of heart disease.")
        advice.append("Consult a doctor to investigate chest pain that may go unnoticed.")

    # Blood pressure advice
    if input_data[3] > 120:
        explanation.append("High resting blood pressure (BP > 120) increases heart disease risk.")
        advice.append("Monitor blood pressure regularly and reduce sodium intake.")

    # Fasting blood sugar advice
    if input_data[5] == 1:
        explanation.append("High fasting blood sugar is linked to heart disease.")
        advice.append("Control blood sugar with a healthy diet and regular exercise.")

    # Heart rate advice
    if input_data[7] < 140:
        explanation.append("Low maximum heart rate is a concern (Heart rate < 140).")
        advice.append("Incorporate cardiovascular exercises to improve heart rate.")

    # Provide general advice
    if not explanation:
        explanation.append("All parameters seem normal.")
        advice.append("Keep maintaining a healthy lifestyle with balanced nutrition and exercise.")

    return explanation, advice

# Home page with model choices
@app.route('/')
def heart():
    return '''
   <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Disease Prediction - Hospitality UI</title>
    <style>
        body {
            font-family: 'Georgia', serif;
            background-size: cover;
            background-position: center;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .overlay {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 50px;
            border-radius: 10px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            text-align: center;
            max-width: 600px;
        }
        h1 {
            font-size: 36px;
            margin-bottom: 20px;
            color: #d2691e;
        }
        p {
            font-size: 18px;
            margin-bottom: 30px;
            color: #333;
        }
        button {
            background-color: #d2691e;
            color: white;
            border: none;
            padding: 15px 30px;
            margin: 10px;
            font-size: 18px;
            cursor: pointer;
            border-radius: 8px;
            transition: background-color 0.3s ease, transform 0.2s ease;
            font-family: 'Georgia', serif;
        }
        button:hover {
            background-color: #b85815;
            transform: scale(1.05);
        }
        @media (max-width: 768px) {
            .overlay {
                width: 100%;
                padding: 20px;
            }
            h1 {
                font-size: 28px;
            }
            button {
                font-size: 16px;
                padding: 12px 24px;
            }
        }
    </style>
</head>
<body>
    <div class="overlay">
        <h1>Welcome to Multiple Disease Prediction</h1>
        <p>Select a service to predict diseases using our advanced machine learning models. We ensure personalized care and accuracy.</p>
        <button onclick="window.location.href='/heart'">Heart Disease Prediction</button>
        <button onclick="window.location.href='/pneumonia'">Pneumonia Prediction</button>

    </div>

</body>
</html>

    '''

# HTML template for input form with hospital-style UI
form_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Heart Disease Prediction</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #f4f4f9, #e9ecef);
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid #e0e0e0;
            transition: box-shadow 0.3s;
        }
        .container:hover {
            box-shadow: 0 6px 40px rgba(0, 0, 0, 0.15);
        }
        h2 {
            text-align: center;
            color: #0056b3;
            font-size: 28px;
            margin-bottom: 20px;
        }
        .form-row {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            margin-bottom: 15px; /* Reduced space between rows */
        }
        .form-group {
            width: calc(48% - 10px); /* Adjusted width for spacing */
            margin-right: 10px; /* Space between columns */
            position: relative;
        }
        .form-group:last-child {
            margin-right: 0; /* Remove margin for the last column */
        }
        label {
            font-weight: bold;
            color: #333;
            display: block;
            margin-bottom: 5px;
        }
        input {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
            transition: border 0.3s, box-shadow 0.3s;
            margin-bottom: 15px; /* Space between label and input */
        }
        input:focus {
            border-color: #0056b3;
            box-shadow: 0 0 5px rgba(0, 86, 179, 0.5);
            outline: none;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #0056b3;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            margin-top: 20px;
            transition: background-color 0.3s, transform 0.3s;
        }
        button:hover {
            background-color: #004494;
            transform: translateY(-1px);
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #888;
        }
         .home-button {
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #0056b3;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        .home-button:hover {
            background-color: #004494;
        }
        .submit-button:disabled {
            background-color: #ccc;
        }
        @media (max-width: 600px) {
            .form-container {
                padding: 15px;
            }
            .submit-button,
            .home-button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Heart Disease Prediction </h2>
        <form action="/predict" method="POST">
            <div class="form-row">
                <div class="form-group">
                    <label for="age">Age:</label>
                    <input type="number" name="age" required>
                </div>
                <div class="form-group">
                    <label for="gender">Gender (1: Male, 0: Female):</label>
                    <input type="number" name="gender" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="cp">Chest Pain Type (1-4):</label>
                    <input type="number" name="cp" required>
                </div>
                <div class="form-group">
                    <label for="trestbps">Resting Blood Pressure:</label>
                    <input type="number" name="trestbps" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="chol">Cholesterol (mg/dl):</label>
                    <input type="number" name="chol" required>
                </div>
                <div class="form-group">
                    <label for="fbs">Fasting Blood Sugar (1: True, 0: False):</label>
                    <input type="number" name="fbs" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="restecg">Resting ECG (0, 1, 2):</label>
                    <input type="number" name="restecg" required>
                </div>
                <div class="form-group">
                    <label for="thalach">Max Heart Rate:</label>
                    <input type="number" name="thalach" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="exang">Exercise Induced Angina (1: Yes, 0: No):</label>
                    <input type="number" name="exang" required>
                </div>
                <div class="form-group">
                    <label for="oldpeak">ST Depression:</label>
                    <input type="number" step="any" name="oldpeak" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="slope">Slope of Peak (1-3):</label>
                    <input type="number" name="slope" required>
                </div>
                <div class="form-group">
                    <label for="ca">Major Vessels (0-3):</label>
                    <input type="number" name="ca" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="thal">Thal (3: normal; 6: fixed defect; 7: reversible defect):</label>
                    <input type="number" name="thal" required>
                </div>
            </div>

            <button type="submit">Predict</button>
            <button type="button" class="home-button" onclick="window.location.href='/'">Home</button>
        </form>
    </div>
    <div class="footer">
        <p>&copy; 2024 Hospital HealthCare System</p>
    </div>
</body>
</html>



'''

# HTML template for result display
result_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Heart Disease - Prediction Result</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 500px;
            margin: 50px auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            border: 1px solid #e0e0e0;
        }
        h2 {
            text-align: center;
            color: #0062cc;
            font-size: 24px;
        }
        p {
            font-size: 18px;
            text-align: center;
        }
        a {
            display: block;
            margin: 20px auto;
            width: 100px;
            padding: 10px;
            text-align: center;
            background-color: #0062cc;
            color: white;
            border-radius: 5px;
            text-decoration: none;
        }
        a:hover {
            background-color: #004a99;
        }
        .advice, .explanation, .disclaimer {
            margin-top: 20px;
            background-color: #f1f1f1;
            padding: 15px;
            border-radius: 5px;
        }
        .home-button {
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #0056b3;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        .home-button:hover {
            background-color: #004494;
        }
        .submit-button:disabled {
            background-color: #ccc;
        }
        @media (max-width: 600px) {
            .form-container {
                padding: 15px;
            }
            .submit-button,
            .home-button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Prediction Result</h2>
        <p>{{ prediction }}</p>

        <div class="explanation">
            <h3>Factors Contributing to Prediction</h3>
            <ul>
                {% for item in explanation %}
                    <li>{{ item }}</li>
                {% endfor %}
            </ul>
        </div>

        <div class="advice">
            <h3>Advice</h3>
            <ul>
                {% for item in advice %}
                    <li>{{ item }}</li>
                {% endfor %}
            </ul>
        </div>

        <div class="disclaimer">
            <strong>Disclaimer:</strong> This prediction is for informational purposes only. Please consult a healthcare professional for a thorough evaluation and personalized advice.
        </div>

        <button type="button" class="home-button" onclick="window.location.href='/heart'">Back</button>
    </div>
</body>
</html>

'''

@app.route('/heart')
def index():
    return render_template_string(form_template)

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from the form
    input_data = [
        int(request.form['age']),
        int(request.form['gender']),
        int(request.form['cp']),
        int(request.form['trestbps']),
        int(request.form['chol']),
        int(request.form['fbs']),
        int(request.form['restecg']),
        int(request.form['thalach']),
        int(request.form['exang']),
        float(request.form['oldpeak']),
        int(request.form['slope']),
        int(request.form['ca']),
        int(request.form['thal'])
    ]

    # Convert input data to a numpy array for prediction
    input_array = np.array([input_data])

    # Make prediction
    prediction = rf.predict(input_array)[0]

    if prediction == 1:
        prediction_text = "There is a high risk of heart disease."
    else:
        prediction_text = "There is a low risk of heart disease."

    # Get explanation and advice
    explanation, advice = get_advice_and_explanation(input_data)

    # Render the result template
    return render_template_string(result_template, prediction=prediction_text, explanation=explanation, advice=advice)

# Pneumonia prediction form
@app.route('/pneumonia')
def pneumonia():
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pneumonia Prediction</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f4f8;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #0056b3;
            margin-bottom: 20px;
        }
        .form-container {
            max-width: 600px;
            margin: auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }
        .form-group {
            margin: 15px 0;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .form-group input,
        .form-group select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
            transition: border-color 0.3s;
        }
        .form-group input:focus,
        .form-group select:focus {
            border-color: #0056b3;
            outline: none;
        }
        .submit-button {
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        .submit-button:hover {
            background-color: #45a049;
        }
        .home-button {
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #0056b3;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        .home-button:hover {
            background-color: #004494;
        }
        .submit-button:disabled {
            background-color: #ccc;
        }
        h1 {
            color: #0056b3;
            margin-bottom: 20px;
            text-align: center; /* Center the heading */
        }
        .error {
            color: red;
            font-size: 12px;
        }
        @media (max-width: 600px) {
            .form-container {
                padding: 15px;
            }
            .submit-button,
            .home-button {
                width: 100%;
            }
        }
    </style>
    <script>
        function validateForm() {
            const name = document.getElementById('name').value;
            const age = document.getElementById('age').value;
            const sex = document.getElementById('sex').value;
            const file = document.getElementById('file').value;

            let valid = true;

            // Clear previous error messages
            document.querySelectorAll('.error').forEach(e => e.textContent = '');

            // Validate name
            if (name.trim() === '') {
                document.getElementById('name-error').textContent = 'Name is required.';
                valid = false;
            }

            // Validate age
            if (age <= 0 || age > 120) {
                document.getElementById('age-error').textContent = 'Please enter a valid age (1-120).';
                valid = false;
            }

            // Validate sex
            if (sex === '') {
                document.getElementById('sex-error').textContent = 'Please select your sex.';
                valid = false;
            }

            // Validate file upload
            if (file === '') {
                document.getElementById('file-error').textContent = 'Please upload a chest X-Ray image.';
                valid = false;
            }

            return valid;
        }
    </script>
</head>
<body>
    <h1>Pneumonia Prediction Using CNN</h1>
    <form id="predict_pneumonia" action="/predict_pneumonia" method="post" enctype="multipart/form-data" onsubmit="return validateForm()">
        <div class="form-container">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
                <span class="error" id="name-error"></span>
            </div>
            <div class="form-group">
                <label for="age">Age:</label>
                <input type="number" id="age" name="age" required>
                <span class="error" id="age-error"></span>
            </div>
            <div class="form-group">
                <label for="sex">Sex:</label>
                <select id="sex" name="sex" required>
                    <option value="" disabled selected>Select your sex</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                </select>
                <span class="error" id="sex-error"></span>
            </div>
            <div class="form-group">
                <label for="file">Upload Chest X-Ray Image:</label>
                <input type="file" id="file" name="file" accept=".png, .jpg, .jpeg" required>
                <span class="error" id="file-error"></span>
            </div>
            <button type="submit" class="submit-button">Predict</button>
            <button type="button" class="home-button" onclick="window.location.href='/'">Home</button>
        </div>
    </form>
</body>
</html>




    '''

# Pneumonia prediction result
@app.route('/predict_pneumonia', methods=['POST'])
def predict_pneumonia_route():
    name = request.form['name']
    age = request.form['age']
    sex = request.form['sex']
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Ensure the uploads folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        result = predict_pneumonia(file_path)
        image_url = url_for('static', filename=f'uploads/{filename}')

        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pneumonia Prediction Result</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f4f8;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #0056b3;
            text-align: center;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }
        .patient-info {
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #e1e1e1;
            border-radius: 5px;
            background-color: #fafafa;
        }
        img {
            display: block;
            margin: 0 auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .result {
            font-size: 1.2em;
            text-align: center;
            margin: 20px 0;
            padding: 10px;
            border: 1px solid #0056b3;
            border-radius: 5px;
            background-color: #e7f3ff;
            color: #0056b3;
        }
        .back-link {
            display: block;
            text-align: center;
            margin-top: 20px;
            text-decoration: none;
            padding: 10px 20px;
            background-color: #0056b3;
            color: white;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .back-link:hover {
            background-color: #004494;
        }
        .disclaimer {
            margin-top: 20px;
            font-size: 0.9em;
            color: #666;
            text-align: center;
            border-top: 1px solid #e1e1e1;
            padding-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Pneumonia Prediction Result</h1>

        <div class="patient-info">
            <p><strong>Name:</strong> {{ name }}</p>
            <p><strong>Age:</strong> {{ age }}</p>
            <p><strong>Sex:</strong> {{ sex }}</p>
        </div>

        <p><img src="{{ image_url }}" alt="Uploaded Image" width="300"></p>

        <div class="result">
            The model predicts: <strong>{{ result }}</strong>
        </div>

        <a class="back-link" href="/pneumonia">Back</a>

        <div class="disclaimer">
            <p><strong>Disclaimer:</strong> This is a project prototype. The results provided by this model are not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.</p>
        </div>
    </div>
</body>
</html>



        ''', name=name, age=age,sex=sex, result=result, image_url=image_url)

    return 'File not allowed'

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



# Start the server
if __name__ == '__main__':
    url = ngrok.connect(5000)
    print(' * Tunnel URL:', url)

    app.run(port=5000)