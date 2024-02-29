from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# Initialize Flask app and Flask-RESTful API
app = Flask(__name__)
api = Api(app)

# Configure SQLAlchemy for SQLite database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
db = SQLAlchemy(app)

# New database schema using SQLAlchemy
class Dataset(db.Model):
    __tablename__ = 'datasets_table'
    DatasetID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Description = db.Column(db.Text)
    Type = db.Column(db.String(100))
    CreationDate = db.Column(db.Date)

# Define output data schema
dataset_fields = {
    'DatasetID': fields.Integer,
    'Name': fields.String,
    'Description': fields.String,
    'Type': fields.String,
    'CreationDate': fields.String  # Assuming date is returned as a string for simplicity
}

# Define request parser for dataset
parser = reqparse.RequestParser()
parser.add_argument('Name', required=True, help="Name cannot be blank")
parser.add_argument('Description')
parser.add_argument('Type', required=True, help="Type cannot be blank")
parser.add_argument('CreationDate', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), help="Date must be in YYYY-MM-DD format")

# Function to get a dataset by ID
def get_dataset(dataset_id):
    dataset = Dataset.query.filter_by(DatasetID=dataset_id).first()
    if dataset:
        # Format the CreationDate to string for simplicity
        return {
            'DatasetID': dataset.DatasetID,
            'Name': dataset.Name,
            'Description': dataset.Description,
            'Type': dataset.Type,
            'CreationDate': dataset.CreationDate.strftime('%Y-%m-%d') if dataset.CreationDate else None
        }
    else:
        return {'error': 'No such dataset found'}, 404

# Resource class for Dataset API
class DatasetAPI(Resource):
    @marshal_with(dataset_fields)
    def get(self, dataset_id):
        return get_dataset(dataset_id)

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
        return get_dataset(dataset_id)

    def delete(self, dataset_id):
        dataset = Dataset.query.filter_by(DatasetID=dataset_id).first()
        if dataset:
            db.session.delete(dataset)
            db.session.commit()
            return {'message': 'Dataset deleted'}
        else:
            return {'error': 'No such dataset found'}, 404

# Register API resource with the Flask application
api.add_resource(DatasetAPI, '/datasets/<int:dataset_id>')

if __name__ == '__main__':
    app.run(debug=True)

