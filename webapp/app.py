from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def getLoginValues():
    username = request.form["Username"]
    password = request.form["password"]
    print("Username = " + username + "  and Password = " + password)
    if(username == "Cochiness" and password == "123"):
        return render_template('loggedUser.html', name = username)
    else:
        return render_template('index.html')



@app.route('/signUp')
def signUp():
    return render_template('signUp.html')
    


if __name__ == '__main__':
    app.run(debug=True)