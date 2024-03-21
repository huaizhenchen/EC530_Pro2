from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'EC530pro2.db')
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class Dataset(db.Model):
    __tablename__ = 'datasets_table'
    DatasetID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Description = db.Column(db.Text)
    Type = db.Column(db.String(100))
    CreationDate = db.Column(db.Date)

dataset_fields = {
    'DatasetID': fields.Integer,
    'Name': fields.String,
    'Description': fields.String,
    'Type': fields.String,
    'CreationDate': fields.String
}

parser = reqparse.RequestParser()
parser.add_argument('Name', required=True, help="Name cannot be blank")
parser.add_argument('Description')
parser.add_argument('Type', required=True, help="Type cannot be blank")
parser.add_argument('CreationDate', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), help="Date must be in YYYY-MM-DD format")

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400
    if file:
        filename = file.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        return jsonify({'message': f'Image {filename} uploaded successfully'}), 200

class DatasetAPI(Resource):
    @marshal_with(dataset_fields)
    def get(self, dataset_id):
        dataset = Dataset.query.filter_by(DatasetID=dataset_id).first()
        if dataset:
            return dataset
        return {'error': 'Dataset not found'}, 404

    @marshal_with(dataset_fields)
    def post(self, dataset_id):
        args = parser.parse_args()
        dataset = Dataset(
            DatasetID=dataset_id,
            Name=args['Name'],
            Description=args.get('Description'),
            Type=args['Type'],
            CreationDate=args.get('CreationDate')
        )
        db.session.add(dataset)
        db.session.commit()
        return dataset, 201

    def delete(self, dataset_id):
        dataset = Dataset.query.filter_by(DatasetID=dataset_id).first()
        if dataset:
            db.session.delete(dataset)
            db.session.commit()
            return {'message': 'Dataset deleted'}, 200
        return {'error': 'Dataset not found'}, 404

api.add_resource(DatasetAPI, '/datasets/<int:dataset_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

