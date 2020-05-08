import os
from flask import Flask, flash, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/home/ubuntu/files"
ALLOWED_EXTENSIONS = {"txt","pdf", "png", "gif", "gpg", "jpeg"}

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
        if 'file' not in request.files:
            return render_template('upload.html',msg="no upload file found", files=request.files)

        file  = request.files['file']

        #check for empty file submission

        if file.filename == '':
           return render_template('upload.html',msg="no File selected")

        if file and allowed_filename(file.filename):
            filename = secure_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return render_template('upload.html',msg="file uploaded succesfully", img_src=UPLOAD_FOLDER+filename)
        else:
            return render_template('upload.html', msg="file extension not allowd")








