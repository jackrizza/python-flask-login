from flask import Flask, render_template, request, Response, redirect
from password import Password

pwd = Password()

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def hello():
        if request.method  == 'POST' :
                email = request.form['email']
                password = request.form['password']
                isAccount = pwd.verifyAccount(email, password)
                if isAccount :
                         return redirect("/woohoo", code=302)
                else :
                        return redirect("/", code=302)
                        
        elif request.method  == 'GET' :
                return render_template('index.html')

@app.route("/signup", methods=['GET','POST'])
def sign():
        if request.method  == 'POST' :
                email = request.form['email']
                password = request.form['password']
                newAccount = pwd.setUser(email, password)
                if newAccount :
                        return redirect("/", code=302)
                else :
                        return redirect("/error", code=302)
        elif request.method  == 'GET' :
                return render_template('sign.html')
@app.route("/error", methods=['GET','POST'])
def error():
        return 'user already exists'

if __name__ == "__main__":
    app.run()