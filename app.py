from flask import Flask,redirect,url_for

app=Flask(__name__)

@app.route('/')
def welcome():
    return 'Welcome to my First App'

@app.route('/success/<name>')
def success(name):
    return 'Welcome '+name

@app.route('/failed/<name>')
def failed(name):
    return 'You dont have access, reach to admin team '+name

@app.route('/dashboard/<nameVal>')
def dashboard(nameVal):
    result=""
    if nameVal == "Ashok":
        result="success"
    else:
        result="failed"

    return redirect(url_for(result,name=nameVal))

if __name__=='__main__':
    app.run(debug=True)
    