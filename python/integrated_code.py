from flask import Flask, request, jsonify
import base64
import os
from flask_cors import CORS
import pymongo
import cv2
import face_recognition
import requests
import numpy as np

app = Flask(__name__)
CORS(app)


connection_string = "mongodb+srv://graphathon:jy3rYESEuOlNFrHl@cluster0.fzt42s2.mongodb.net/tracker"
client = pymongo.MongoClient(connection_string)
dbs = client['tracker']
info = dbs.buses

# Function to save image
def save_image(image_data, phone_no):
    image_data = image_data.split(",")[1]  # Remove the base64 prefix
    # Convert base64 to binary
    image_binary = base64.b64decode(image_data)
    # Define the path for saving the image
    save_path = f"login/{phone_no}_userImage.jpg"
    if not os.path.exists('login'):
        os.makedirs('login')
    # Save the image
    with open(save_path, 'wb') as f:
        f.write(image_binary)
    return save_path

# Function to compare image with saved images
def compare_with_saved_images(url_encoding):
    folder_path = "login/"  # Folder where multiple saved images are present
    # Get the list of files in the folder
    file_names = os.listdir(folder_path)
    # Filter only image files
    image_files = [file_name for file_name in file_names if file_name.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    # Compare the URL image with each saved image until a match is found
    for image_file in image_files:
        img2 = cv2.imread(os.path.join(folder_path, image_file))
        rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        saved_encoding = face_recognition.face_encodings(rgb_img2)[0]
        result = face_recognition.compare_faces([url_encoding], saved_encoding)[0]
        if result:
            return True
    return False

# Route to save image
@app.route('/save-image', methods=['POST'])
def save_image_route():
    data = request.get_json()
    phone_no = data["phoneNo"]
    image_data = data['image']
    save_path = save_image(image_data, phone_no)
    return jsonify({"message": "Image saved successfully!", "save_path": save_path})

# Route to compare image
@app.route('/compare-image', methods=['POST'])
def compare_image_route():
    data = request.get_json()
    url = data["imageUrl"]
    response = requests.get(url)
    img_array = np.array(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    url_encoding = face_recognition.face_encodings(rgb_img)[0]
    match_found = compare_with_saved_images(url_encoding)
    return jsonify({"match_found": match_found})

if __name__ == '__main__':
    app.run(debug=True)
