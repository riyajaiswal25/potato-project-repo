from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Set the upload folder for images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file extension is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the 'image' key exists in the request files
    if 'image' not in request.files:
        return jsonify({'message': 'No image provided in the request.'}), 400

    image = request.files['image']

    # Check if the file is not empty and has an allowed extension
    if image.filename == '' or not allowed_file(image.filename):
        return jsonify({'message': 'Invalid image file.'}), 400

    # Save the image file to the upload folder
    filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(filename)

    # Send the image to the backend for prediction
    url = 'http://0.0.0.0:8000/predict'
    files = {'image': open(filename, 'rb')}
    response = requests.post(url, files=files)

    # Remove the uploaded image after sending it to the backend
    os.remove(filename)

    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(port=8001)  # Run the Flask app on a different port (e.g., 8001) to avoid conflict with the frontend
