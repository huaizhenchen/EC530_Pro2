from flask import Flask, request, jsonify, send_from_directory
import logging
import os
import cProfile
import pstats
import io

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json', 'xls', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure logging
logging.basicConfig(level=logging.INFO, filename='api.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def profile(f):
    """Decorator to add cProfile profiling to any function."""
    def wrap(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = f(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        logging.info(s.getvalue())
        return result
    return wrap

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    logging.info("Upload file request received")
    if 'file' not in request.files:
        logging.error("No file part in the request")
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        logging.error("No selected file")
        return jsonify(error="No selected file"), 400
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        logging.info(f"File {filename} uploaded successfully")
        return jsonify(message=f"File {filename} uploaded successfully"), 200
    else:
        logging.error("File type not allowed")
        return jsonify(error="File type not allowed"), 400

@app.route('/files', methods=['GET'])
def list_files():
    logging.info("Listing uploaded files")
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    logging.info("Uploaded files listed successfully")
    return jsonify(files=files), 200

@app.route('/files/<filename>', methods=['GET'])
def preview_file(filename):
    logging.info(f"Previewing file {filename}")
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logging.error(f"Error previewing file {filename}: {str(e)}")
        return jsonify(error="File not found"), 404

@app.route('/train', methods=['POST'])
def train_model():
    logging.info("Training model request received")
    # Simulate training model
    logging.info("Model training started")
    # After training completes
    logging.info("Model training completed successfully")
    return jsonify(message="Model trained successfully"), 200

@app.route('/cancel-training', methods=['POST'])
def cancel_training():
    logging.info("Cancel training request received")
    # Simulate cancel training
    logging.info("Training cancelled successfully")
    return jsonify(message="Training cancelled"), 200

@app.route('/training-progress', methods=['GET'])
def training_progress():
    logging.info("Checking training progress")
    # Simulate checking progress
    progress = "50%"  # Example progress
    logging.info(f"Training progress: {progress}")
    return jsonify(progress=progress), 200

@app.route('/file-type', methods=['POST'])
def select_file_type():
    logging.info("File type selection request received")
    file_type = request.json.get('type', '')
    if file_type.lower() in ALLOWED_EXTENSIONS:
        logging.info(f"File type {file_type} selected successfully")
        return jsonify(message=f"File type {file_type} selected"), 200
    else:
        logging.error("Invalid file type selected")
        return jsonify(error="Invalid file type"), 400

@app.route('/labels', methods=['GET'])
def check_labels():
    logging.info("Checking labels of uploaded data")
    # Simulate label checking
    labels = ["label1", "label2"]  # Example labels
    logging.info("Labels checked successfully")
    return jsonify(labels=labels), 200

@app.route('/adjust-algorithm', methods=['POST'])
def adjust_training_algorithm():
    logging.info("Adjusting training algorithm request received")
    # Simulate algorithm adjustment
    algorithm = request.json.get('algorithm', '')
    logging.info(f"Algorithm {algorithm} selected successfully")
    return jsonify(message=f"Algorithm {algorithm} adjusted"), 200

@app.route('/add-data', methods=['POST'])
def add_training_data():
    logging.info("Adding training data request received")
    # Simulate adding data
    logging.info("Training data added successfully")
    return jsonify(message="Training data added"), 200

@app.route('/restart-training', methods=['POST'])
def restart_training():
    logging.info("Restarting training process")
    # Simulate restarting training
    logging.info("Training process restarted successfully")
    return jsonify(message="Training restarted"), 200

@app.route('/compare-models', methods=['GET'])
def compare_models():
    logging.info("Comparing models' performances")
    # Simulate model comparison
    models_performance = {"model1": 0.95, "model2": 0.92}  # Example performance
    logging.info("Models compared successfully")
    return jsonify(models_performance=models_performance), 200

if __name__ == '__main__':
    app.run(debug=True)
