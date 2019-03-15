from flask import Flask, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy



app = Flask (__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chimtech:chimtech@localhost:8889/chimtech'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'f8wv3w2f>v9j4sEuhcNYydAGMzzZJgkGgyHE9gUqaJcCk^f*^o7fQyBT%XtTvcYM'



@app.route("/")
def index():
    return render_template("index.html")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    valid_username  = ''
    valid_password = ''
    username = ''
    

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:

            if len(username) < 4:
                valid_username = "Not a valid username"
            
            if len(password) < 4 or password != verify:
                valid_password = "Not a valid password"

            if valid_username=="" and valid_password=="":
                new_user = User(username = username, password = password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/welcome')
                
        else:
            valid_username = 'Duplicate user'

    return render_template('signup.html', valid_username=valid_username, username=username , valid_password=valid_password)


@app.route('/welcome', methods=['POST', 'GET'])
def welcome():   
    username = request.form.get('username')
    username = request.args.get('username')
    return render_template(('welcome.html'),username = username)

@app.route('/login', methods= (['GET','POST']))
def login():
    valid_username  = ''
    valid_password = ''
    username = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username 
            return redirect('/welcome')
        if not user:
            valid_username = "Not a valid username"
        if user and not user.password == password:
            valid_password = "Not a valid password"
            
        
            return render_template('login.html', valid_username=valid_username, username=username , valid_password=valid_password)


    
if __name__ == '__main__':
    app.run()
