import os

from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

#UPLOAD_FOLDER = '/static/images/uploads/'
#UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/static/images/uploads/'
# check if uploaded file has allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#API

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def getLoginValues():
    username = request.form["Username"]
    password = request.form["password"]
    print("Username = " + username + "  and Password = " + password)
    if(username == "Cochiness" and password == "123"):
        return render_template('loggedUser.html', name=username)
    else:
        return render_template('index.html')


@app.route('/submit_expression', methods=['POST'])
def submit_expression():
    expression = request.form["symbolic_expression"]
    print("L'espressione del cazzo è = " + expression)
    return render_template('loggedUser.html', expression="expression")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if post request contains the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('uploaded_file', filename=filename))



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



if __name__ == '__main__':
    app.run(debug=True)
