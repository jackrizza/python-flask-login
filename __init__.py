from flask import Flask, render_template, request, Response, redirect
from password import Password

account = Password()

app = Flask(__name__)

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

@app.route("/signup/<error>", methods=['GET','POST'])
def sign(error=None):
        if request.method  == 'POST' :
                email = request.form['email']
                password = request.form['password']
                newAccount = account.setUser(email, password)
                if newAccount :
                        return redirect("/", code=302)
                else :
                        return redirect("/signup/already", code=302)
        elif request.method  == 'GET' :
                return render_template('sign.html', error=error)

if __name__ == "__main__":
    app.run()