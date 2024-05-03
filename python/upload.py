from flask import Flask, request, jsonify
import base64
import os
from flask_cors import CORS
import pymongo

app = Flask(__name__)
CORS(app)

connection_string="mongodb+srv://graphathon:jy3rYESEuOlNFrHl@cluster0.fzt42s2.mongodb.net/tracker"

client=pymongo.MongoClient(connection_string)

dbs=client['tracker']
info=dbs.buses

@app.route('/save-image', methods=['POST'])
def save_image():
    data = request.get_json()
    a=data["phoneNo"]
    image_data = data['image']
    print(a)
    b="sw"
    for record in info.find({'driver.contactInfo':a}):
        b=record

    print(b["photo"]["secure_url"])

    image_data = image_data.split(",")[1]  # Remove the base64 prefix

    # Convert base64 to binary
    image_binary = base64.b64decode(image_data)

    # Define the path for saving the image
    save_path = "login/userImage.jpg"
    if not os.path.exists('login'):
        os.makedirs('login')

    # Save the image
    with open(save_path, 'wb') as f:
        f.write(image_binary)

    return jsonify({"message": "Image saved successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
