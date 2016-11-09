from flask import Flask, render_template, request, Response, redirect
from password import Password
from twoFact import tf
from db import DB

app = Flask(__name__)
account = Password()
tf = tf()
db = DB()

@app.route("/", methods=['GET','POST'])
def hello():
        if request.method  == 'POST' :
                email = request.form['email']
                password = request.form['password']
                isAccount = account.verifyAccount(email, password)
                if isAccount :
                         return redirect("/woohoo", code=302)
                else :
                        return redirect("/", code=302)
                        
        elif request.method  == 'GET' :
                return render_template('index.html')

@app.route("/signup/<step>", methods=['GET','POST'])
def sign(step=None):
        global db
        if step == "1" :
                if request.method  == 'POST' :
                        email = request.form['email']
                        password = request.form['password']
                        newAccount = db.setUser(email, password)
                        if newAccount :
                                return redirect("/signup/2", code=302)
                        else :
                                return redirect("/signup/already", code=302)
                elif request.method  == 'GET' :
                        return render_template('sign.html', error="already")
        elif step == "2" :
                if request.method  == 'POST' :
                        phone = request.form['phone']
                        tf.sendMessage(phone)
                elif request.method  == 'GET' :
                        return render_template('phone.html')

if __name__ == "__main__":
    app.run()