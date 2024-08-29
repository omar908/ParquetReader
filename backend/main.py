import os
import logging
import duckdb
# import pandas as pd
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'parquet'}

# Create instance of Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Basic logging configuration
logging.basicConfig(level=logging.DEBUG,  # Set the logging level to DEBUG
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/file/parquet/sample", methods=['GET'])
def get_sample_data():
    # Connect to DuckDB
    con = duckdb.connect()

    # Query Parquet file and convert result to DataFrame
    df = con.execute("SELECT * FROM read_parquet('./test-data/sample1.parquet')").df()

    # Convert DataFrame to JSON-compatible format (dictionary) -> to JSON
    return jsonify(df.to_dict(orient='records'))

@app.route("/file/parquet", methods=['POST'])
def convert_parquet_to_json():
    logger.debug("Handling POST request for /file/parquet")
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    logger.debug(f"Validating file.filename: {file.filename}")
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            logger.debug("Creating Directory: " + app.config['UPLOAD_FOLDER'])
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logger.debug(f"Saving File to: {file_path}")
        file.save(file_path)

        # Connect to DuckDB
        con = duckdb.connect()

        # Query Parquet file and convert result to DataFrame
        select_query = f"SELECT * FROM read_parquet('{file_path}')"
        logger.debug(f'select_query to execute: {select_query}')
        df = con.execute(select_query).df()

        # Convert DataFrame to JSON-compatible format (dictionary) -> to JSON
        return jsonify(df.to_dict(orient='records'))

    logger.error('Something failed during file processing')
    return jsonify({'error': 'Oops, something failed... Sorry!'}), 500
