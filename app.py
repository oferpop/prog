from flask import Flask, request, jsonify, send_from_directory ,render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)

UPLOAD_FOLDER = 'backend/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

from flask import send_from_directory

class Hello(Resource):
    def get(self):
        return send_from_directory('../frontend', 'index.html')  # Adjusted path


class UploadImage(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"error": "No file part"}, 400

        file = request.files['file']
        if file.filename == '':
            return {"error": "No selected file"}, 400

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {"message": "File uploaded successfully", "filename": filename}, 200

class ListImages(Resource):
    def get(self):
        images = os.listdir(app.config['UPLOAD_FOLDER'])
        image_urls = [f"http://127.0.0.1:5000/static/uploads/{image}" for image in images]
        return {"images": image_urls}

api.add_resource(Hello, '/')
api.add_resource(UploadImage, '/upload')
api.add_resource(ListImages, '/images')

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

# 66666