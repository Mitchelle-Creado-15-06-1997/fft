from flask import Flask, render_template, request, session
import pandas as pd
import os
from werkzeug.utils import secure_filename
import numpy as np
from matplotlib import pyplot as plt
import csv

#*** Flask configuration
 
# Define folder to save uploaded files to process further
UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
 
# Define allowed files (for this example I want only csv file)
ALLOWED_EXTENSIONS = {'csv'}
 
app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'
 
 
@app.route('/')
def index():
    return render_template('fft.html')
 
@app.route('/',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # upload file flask
        uploaded_df = request.files['uploaded-file']
 
        # Extracting uploaded data file name
        data_filename = secure_filename(uploaded_df.filename)
 
        # flask upload file to database (defined uploaded folder in static path)
        uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
 
        # Storing uploaded file path in flask session
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
 
        return render_template('fft.html')
 
@app.route('/fft')
def showData():
    with open(os.path.join('./staticFiles/uploads/sheets.csv'), newline='') as csvfile:
        list_data = list(csv.reader(csvfile))

        list_to_arr = np.array(list_data)

    squareimpulse = list_to_arr.flatten()
    # squareimpulse = np.array([0,0,0,0,0,1,1,1,1,1,0,0,0,0,0])

    img = (squareimpulse)
    f = np.fft.fft(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = (np.abs(fshift))
    # plt.plt.switch_backend('Agg') 
    plt.switch_backend('agg')
    plt.subplot(121)
    plt.plot(img)
    plt.title('Input Image')
    plt.xticks([]), plt.yticks([])

    plt.subplot(122)
    plt.plot(magnitude_spectrum)
    plt.title('Magnitude Spectrum')
    plt.xticks([]), plt.yticks([])
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude')
    file_name = os.path.join(app.config['UPLOAD_FOLDER'] + '/my_plot.png')
    plt.savefig(file_name)
    # plt.show()
    # // end

    # Retrieving uploaded file path from session
    # data_file_path = session.get('uploaded_data_file_path', None)
 
    # read csv file in python flask (reading uploaded csv file from uploaded server location)
    # uploaded_df = pd.read_csv(data_file_path)
 
    # pandas dataframe to html table flask
    # uploaded_df_html = uploaded_df.to_html()
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'my_plot.png')
    return render_template('show_csv_data.html', user_image = full_filename)
 
@app.route('/back')
def back():
    return render_template('fft.html')

if __name__=='__main__':
    app.run(host='127.0.0.1', port=5005, debug = True)