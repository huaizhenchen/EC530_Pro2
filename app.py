from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EC530pro2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# Data model definitions
class Dataset(db.Model):
    __tablename__ = 'datasets_table'
    DatasetID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Description = db.Column(db.Text)
    Type = db.Column(db.String(100))
    CreationDate = db.Column(db.Date)

class Image(db.Model):
    __tablename__ = 'images_table'
    ImageID = db.Column(db.Integer, primary_key=True)
    DatasetID = db.Column(db.Integer, db.ForeignKey('datasets_table.DatasetID'))
    FilePath = db.Column(db.Text)
    Label = db.Column(db.String(255))
    Split = db.Column(db.String(50))

class Annotation(db.Model):
    __tablename__ = 'annotations_table'
    AnnotationID = db.Column(db.Integer, primary_key=True)
    ImageID = db.Column(db.Integer, db.ForeignKey('images_table.ImageID'))
    ObjectClass = db.Column(db.String(100))
    BoundingBox = db.Column(db.String(100))

class Model(db.Model):
    __tablename__ = 'models_table'
    ModelID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Architecture = db.Column(db.String(100))
    CreationDate = db.Column(db.Date)
    TrainingDatasetID = db.Column(db.Integer, db.ForeignKey('datasets_table.DatasetID'))

class TrainingSession(db.Model):
    __tablename__ = 'training_sessions_table'
    SessionID = db.Column(db.Integer, primary_key=True)
    ModelID = db.Column(db.Integer, db.ForeignKey('models_table.ModelID'))
    StartDate = db.Column(db.DateTime)
    EndDate = db.Column(db.DateTime)
    Status = db.Column(db.String(50))
    Accuracy = db.Column(db.Float)
    Loss = db.Column(db.Float)

class Inference(db.Model):
    __tablename__ = 'inferences_table'
    InferenceID = db.Column(db.Integer, primary_key=True)
    ModelID = db.Column(db.Integer, db.ForeignKey('models_table.ModelID'))
    InputData = db.Column(db.Text)
    Result = db.Column(db.Text)
    InferenceDate = db.Column(db.DateTime)


class DatasetResource(Resource):
    # Get a single dataset
    def get(self, dataset_id):
        dataset = Dataset.query.get(dataset_id)
        if dataset:
            return {
                'DatasetID': dataset.DatasetID,
                'Name': dataset.Name,
                'Description': dataset.Description,
                'Type': dataset.Type,
                'CreationDate': dataset.CreationDate.isoformat() if dataset.CreationDate else None
            }
        return {'message': 'Dataset not found'}, 404

    # Delete a single dataset
    def delete(self, dataset_id):
        dataset = Dataset.query.get(dataset_id)
        if dataset:
            db.session.delete(dataset)
            db.session.commit()
            return {'message': 'Dataset deleted.'}, 200
        return {'message': 'Dataset not found'}, 404

    # Update a single dataset
    def put(self, dataset_id):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str, required=True, help="Name cannot be blank.")
        parser.add_argument('Description', type=str)
        parser.add_argument('Type', type=str)
        parser.add_argument('CreationDate', type=lambda x: datetime.strptime(x, '%Y-%m-%d'))
        args = parser.parse_args()

        dataset = Dataset.query.get(dataset_id)
        if dataset:
            dataset.Name = args['Name']
            dataset.Description = args.get('Description', dataset.Description)
            dataset.Type = args.get('Type', dataset.Type)
            dataset.CreationDate = args.get('CreationDate', dataset.CreationDate)
            db.session.commit()
            return {'message': 'Dataset updated.'}, 200
        return {'message': 'Dataset not found'}, 404


# Flask-RESTful resource for handling the dataset collection
class DatasetListResource(Resource):
    # Get all datasets
    def get(self):
        datasets = Dataset.query.all()
        return [{'DatasetID': d.DatasetID, 'Name': d.Name, 'Description': d.Description, 'Type': d.Type,
                 'CreationDate': d.CreationDate.isoformat() if d.CreationDate else None} for d in datasets]

    # Create a new dataset
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str, required=True, help="Name cannot be blank.")
        parser.add_argument('Description', type=str)
        parser.add_argument('Type', type=str)
        parser.add_argument('CreationDate', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=False)
        args = parser.parse_args()

        dataset = Dataset(Name=args['Name'], Description=args['Description'], Type=args['Type'],
                          CreationDate=args.get('CreationDate'))
        db.session.add(dataset)
        db.session.commit()
        return {'message': 'Dataset created.', 'DatasetID': dataset.DatasetID}, 201


# Adding resources to the API
api.add_resource(DatasetListResource, '/datasets')
api.add_resource(DatasetResource, '/datasets/<int:dataset_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)