import datetime as dt
import os

from flask import Flask, jsonify, make_response, render_template, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

import analysis
from random_token import random_token

TOKEN_SIZE = 16
ALLOWED_IMAGE_EXTENSIONS = set(['xlsx'])
UPLOAD_FOLDER = 'userreports'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app, origins=["http://localhost:5000"])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Max upload size 2 MegaBytes


@app.route("/")
def helloWorld():
  return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


@app.route('/uploadreport', methods=['POST'])
def upload_report():

    # check if the post request has the file part
    if 'file' not in request.files:
        return make_response("No file was sent!", 400)

    files = request.files.getlist('file')
    if request.files['file'].filename == '':
        return make_response("No file selected!", 400)

    my_token = random_token(N=TOKEN_SIZE)
    DATE = dt.datetime.now().strftime("%d-%m-%Y")
    FOLDER = app.config['UPLOAD_FOLDER'] +"/"+DATE+"/"+ my_token + "/pnlreport"
    os.makedirs(FOLDER, exist_ok=True)
    
    print("files :",files)

    report_filename = None

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            report_filepath = os.path.join(FOLDER, filename)
            report_filename = my_token + "/pnlreport/" + filename
            file.save(report_filepath)

    return jsonify(report_filepath=report_filename)


@app.route('/analyze/<string:token>/pnlreport/<string:filename>', methods=['GET'])
def generate_analysis(token: str, filename: str):

    report_filename = token + "/pnlreport/" + filename

    DATE = dt.datetime.now().strftime("%d-%m-%Y")
    FOLDER = app.config['UPLOAD_FOLDER'] +"/"+DATE
    report_filepath = os.path.join(FOLDER, report_filename)

    print("Run analysis on report :", report_filepath)

    result = analysis.main(report_filepath)

    return render_template('report.html', data=result)


if __name__ == "__main__":

    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True)
