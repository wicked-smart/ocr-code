import os
from flask import Flask, flash, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

from ocr_core import ocr_core

UPLOAD_FOLDER = "/home/ubuntu/files/"
ALLOWED_EXTENSIONS = {"txt","pdf", "png", "gif", "jpg", "jpeg"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#check for allowed filenames
def allowed_filename(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file',methods=['GET','POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        # check if the post request has the file part

        file  = request.files['file']

        #check for empty file submission

        if file.filename == '':
           return render_template('upload.html',msg="no File selected")


        if file and allowed_filename(file.filename):

            file_name = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name))
            try:
                extracted_text = ocr_core(UPLOAD_FOLDER + file_name)
                print(extracted_text)
            except:
                print("error in file extraction")

            return render_template('upload.html',msg="file uploaded succesfully",  img_src= UPLOAD_FOLDER + file_name)

        else:

            return render_template('upload.html', msg="file extension not allowd")








