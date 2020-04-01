import os
from flask import Flask, render_template, jsonify, send_from_directory, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

#UPLOAD_FOLDER = '/static/images/uploads/'
#UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
#app.config['UPLOAD_FOLDER'] = base_folder_image


# check if uploaded file has allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




# API

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
        return render_template('index.html', message = "error")


@app.route('/submit_expression', methods=['POST'])
def submit_expression():
    expression = request.form["symbolic_expression"]
    print("L'espressione del cazzo è = " + expression)
    return render_template('loggedUser.html', expression="expression")



#  API - DRAG AND DROP POST FILE TO SERVER
@app.route("/sendfile", methods=["POST"])
def send_file():
    fileob = request.files["file2upload"]
    filename = secure_filename(fileob.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)
    # open and close to update the access time.
    with open(save_path, "r") as f:
        pass
    return "successful_upload"



# GET NAME OF UPLOADED FILES
@app.route("/filenames", methods=["GET"])
def get_filenames():
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])
    def modify_time_sort(file_name):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
        file_stats = os.stat(file_path)
        last_access_time = file_stats.st_atime
        return last_access_time

    filenames = sorted(filenames, key=modify_time_sort)
    return_dict = dict(filenames=filenames)
    return jsonify(return_dict)


if __name__ == '__main__':
    app.run(debug=True)
