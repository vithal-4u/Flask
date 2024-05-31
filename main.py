from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/success/<name>')
def success(name):
    return render_template('result.html',result=name)

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


@app.route('/submit_registration',methods=['POST','GET'])
def submit_registration():
    details=""
    if request.method == 'POST':
       name = request.form['name']
       gender = request.form['gender']
       phone = request.form['phone']
       year = request.form['year']
       details = name + " is registered to RCC, any support will reach to "+ phone
       
    return redirect(url_for('success',name=details))
    

if __name__=='__main__':
    app.run(debug=True)
    