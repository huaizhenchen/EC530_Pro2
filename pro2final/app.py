from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import torch
from torchvision import models, transforms
import os
from datetime import datetime
from PIL import Image
import json
import urllib.request

app = Flask(__name__)
api = Api(app)
model = models.resnet50(pretrained=True)
model.eval()


transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def load_imagenet_classes():
    class_idx_url = "https://storage.googleapis.com/download.tensorflow.org/data/imagenet_class_index.json"
    with urllib.request.urlopen(class_idx_url) as url:
        class_idx = json.loads(url.read().decode())
        class_labels = {int(key): value[1] for key, value in class_idx.items()}
    return class_labels

imagenet_classes = load_imagenet_classes()

def classify_image(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)
    with torch.no_grad():
        output = model(image)
    prediction = output.argmax(dim=1).item()
    predicted_class = imagenet_classes[prediction]
    return predicted_class
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'EC530pro2.db')
db = SQLAlchemy(app)

# Upload folder configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database model
class Dataset(db.Model):
    __tablename__ = 'datasets_table'
    DatasetID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Description = db.Column(db.Text)
    Type = db.Column(db.String(100))
    CreationDate = db.Column(db.Date)

# Fields for serialization
dataset_fields = {
    'DatasetID': fields.Integer,
    'Name': fields.String,
    'Description': fields.String,
    'Type': fields.String,
    'CreationDate': fields.String
}

# Argument parsing
parser = reqparse.RequestParser()
parser.add_argument('Name', required=True, help="Name cannot be blank")
parser.add_argument('Description')
parser.add_argument('Type', required=True, help="Type cannot be blank")
parser.add_argument('CreationDate', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), help="Date must be in YYYY-MM-DD format")

# Route for uploading images
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        class_id = classify_image(save_path)
        print("file is classified, class ID:", class_id)
        new_dataset = Dataset(Name=filename, Description=f'Classified image with class ID: {class_id}', Type='Image', CreationDate=datetime.today().date())
        db.session.add(new_dataset)
        db.session.commit()
        return jsonify({'message': f'Image {filename} uploaded and classified successfully'}), 200
# Resource for handling datasets
class DatasetAPI(Resource):
    @marshal_with(dataset_fields)
    def get(self, dataset_id):
        dataset = Dataset.query.filter_by(DatasetID=dataset_id).first()
        if not dataset:
            return {'error': 'Dataset not found'}, 404
        return dataset

    def put(self, dataset_id):
        dataset = Dataset.query.get(dataset_id)
        if not dataset:
            return {'error': 'Dataset not found'}, 404

        args = parser.parse_args()
        has_update = False

        if 'Name' in args and args['Name'] is not None:
            dataset.Name = args['Name']
            has_update = True
        if 'Description' in args and args['Description'] is not None:
            dataset.Description = args['Description']
            has_update = True
        if 'Type' in args and args['Type'] is not None:
            dataset.Type = args['Type']
            has_update = True
        if 'CreationDate' in args and args['CreationDate'] is not None:
            dataset.CreationDate = args['CreationDate']
            has_update = True

        if has_update:
            db.session.commit()
            return {'message': 'Dataset updated successfully'}, 200
        else:
            return {'message': 'No update performed'}, 200
    @marshal_with(dataset_fields)  
    def post(self):
        args = parser.parse_args()
        new_dataset = Dataset(Name=args['Name'], Description=args.get('Description'), Type=args['Type'], CreationDate=args.get('CreationDate'))
        db.session.add(new_dataset)
        db.session.commit()
        return new_dataset, 201 

    def delete(self, dataset_id):
        dataset = Dataset.query.get(dataset_id)
        if dataset:
            db.session.delete(dataset)
            db.session.commit()
            return {'message': 'Dataset deleted'}, 200
        return {'error': 'Dataset not found'}, 404

# Adding resources to API
api.add_resource(DatasetAPI, '/datasets/', '/datasets/<int:dataset_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


