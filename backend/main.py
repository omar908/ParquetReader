import os
import logging
import duckdb
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'parquet'}
NO_FILES_HAVE_BEEN_UPLOADED = 'No files have been yet uploaded'

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

@app.route("/file/parquet/list", methods=['GET'])
def get_uploaded_parquet_list():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        logger.debug('Upload Directory does not exist, no files uploaded')
        return jsonify({'error': NO_FILES_HAVE_BEEN_UPLOADED}), 404
    
    try:
        list_of_files = os.listdir(app.config['UPLOAD_FOLDER'])
        logger.debug(f"List of files within {app.config['UPLOAD_FOLDER']}, are {list_of_files}, with a size of {len(list_of_files)}")
        if len(list_of_files) == 0:
            return jsonify({'error': NO_FILES_HAVE_BEEN_UPLOADED}), 404
        filtered_files = [fileName for fileName in list_of_files if allowed_file(fileName)]
        logger.debug(f"Filtered list {filtered_files}, with a size of {len(filtered_files)}")
        return jsonify(filtered_files)
    except Exception as e:
        logger.error(f"Error accessing files: {str(e)}")
        return jsonify({'error': 'Unable to access files'}), 500

@app.route("/file/parquet", methods=['GET'])
def search_uploaded_parquet_files():
    query_filename = request.args.get('filename')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        logger.debug('Upload Directory does not exist, no files uploaded')
        return jsonify({'error': NO_FILES_HAVE_BEEN_UPLOADED}), 404

    if trim_and_check_if_blank(query_filename):
        logger.debug(f'Empty filename query parameter: {query_filename}')
        return jsonify({'error': 'Empty or missing filename query parameter'}), 400

    if not allowed_file(query_filename):
        logger.debug(f'Invalid file type, filename: {query_filename}')
        return jsonify({'error': f'Invalid File Type: {query_filename}, file type support: {ALLOWED_EXTENSIONS}'}), 400

    try:
        list_of_files = os.listdir(app.config['UPLOAD_FOLDER'])
        filtered_files = [fileName for fileName in list_of_files if query_filename in fileName]
        logger.debug(f"Files found: {filtered_files}, Lenght of list: {len(filtered_files)}")
        if len(filtered_files) == 0:
            return jsonify({'error': 'No matching files found'}), 404

        return get_parquet_file_content(query_filename, app.config['UPLOAD_FOLDER'])
    except Exception as e:
        logger.error(f"Error accessing files: {str(e)}")
        return jsonify({'error': 'Unable to access files'}), 500

@app.route("/file/parquet/sample", methods=['GET'])
def get_sample_data():
    return get_parquet_file_content('sample1.parquet', './test-data')

@app.route("/file/parquet", methods=['POST'])
def convert_parquet_to_json():
    try:
        logger.debug("Handling POST request for /file/parquet")
        if 'file' not in request.files:
            return jsonify({'error': 'No file attached to request'}), 400

        file = request.files['file']

        logger.debug(f"Validating file.filename: {file.filename}")
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid File Type'}), 400

        filename = secure_filename(file.filename)
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            logger.debug("Creating Directory: " + app.config['UPLOAD_FOLDER'])
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logger.debug(f"Saving File to: {file_path}")
        file.save(file_path)

        return get_parquet_file_content(filename, app.config['UPLOAD_FOLDER'])

    except Exception as e:
        logger.error(f'Something failed during file processing: {str(e)}')
        return jsonify({'error': 'Oops, something failed... Sorry!'}), 500

def trim_and_check_if_blank(string):
    # Check if string is None
    if string is None:
        return True

    trimmed_string = string.strip()
    return not trimmed_string

def get_parquet_file_content(file_name, directory_path):
    file_path = os.path.join(directory_path, file_name)

    # Connect to DuckDB
    con = duckdb.connect()

    # Logging Query
    select_query = f"SELECT * FROM read_parquet('{file_path}')"
    logger.debug(f'select_query to execute: {select_query}')

    # Query Parquet file and convert result to DataFrame
    df = con.execute(select_query).df()

    # Convert DataFrame to JSON-compatible format (dictionary) -> to JSON
    return jsonify(df.to_dict(orient='records'))