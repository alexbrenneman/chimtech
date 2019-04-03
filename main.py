from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

error = False

app = Flask (__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chimtech:chimtech@localhost:8889/chimtech'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'f8wv3w2f>v9j4sEuhcNYydAGMzzZJgkGgyHE9gUqaJcCk^f*^o7fQyBT%XtTvcYM'



@app.route("/")
def index():
    error = False
    return render_template("index.html")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(150))


def symbol(parameter):
    if parameter.count("@") == 1 and parameter.count(".") ==1 :
        return True
    else:
        return False

# Check for spaces in function, returning True if there are no spaces
def no_space(parameter):
    if parameter.count(" ") == 0:
        return True    
    else:
        return False

def mysession():
     mysession = session.get('username', None)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    valid_username  = ''
    valid_password = ''
    username = ''
    email = ''
    valid_email = ''
    
    

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:

            if len(username) < 1:
                valid_username = "Not a valid username"
            
            if len(password) < 4 or password != verify:
                valid_password = "Not a valid password"

            if len(email) and symbol(email) and no_space(email) or email == "":
                valid_email = ""
            else:
                valid_email = "Not a valid email"
        else:
            valid_username = 'Duplicate user'
        

        if valid_username=="" and valid_password=="" and valid_email=="":
            new_user = User(username = username, password = password, email = email)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return render_template('/welcome.html',username = username, email = email)
                
        

    return render_template('signup.html', valid_username=valid_username, username=username , valid_password=valid_password , email=email)

@app.route('/profile', methods=['POST','GET'])
def profile():
    username = request.form.get('username')
    email = request.form.get('email')
    
    return render_template(("/profile.html"),username = username, email = email)

@app.route('/welcome', methods=['POST', 'GET'])
def welcome():   
    username = request.form.get('username')
    email = request.form.get('email')
    return render_template(('welcome.html'),username = username, email = email)

@app.route('/login', methods= ['GET','POST'])
def login():
    error = False
    valid_username  = 'Not valid username'
    valid_password = 'Not valid password'
    username = ''
    email=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if username == "" or password == "":
            return render_template('login.html', valid_username=valid_username, valid_password=valid_password, error=True)
        else:
            if user.username == username and user.password == password:
                session['username'] = username 
                error = False
                return render_template('/welcome.html', username = username, email = user.email)
        
        
           
    return render_template('login.html', valid_username=valid_username, valid_password=valid_password, error=False)


@app.route('/reviews')
def service():
    return render_template('reviews.html')

@app.route('/cleaning_reviews')
def cleaning_reviews():
    return render_template('cleaning-reviews.html')

@app.route('/restoration_reviews')
def restoration_reviews():
    return render_template('restoration_reviews.html')

@app.route('/inspection_reviews')
def inspection_reviews():
    return render_template('inspection_reviews.html')

@app.route('/construction_reviews')
def construction_reviews():
    return render_template('construction_reviews.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')
        
  


class Companies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    street = db.Column(db.String(120))
    city = db.Column(db.String(120))
    zip_code = db.Column(db.Integer)

    

@app.route('/add_companies', methods = ['POST','GET'])
def add_companies():
    '''valid_name = ""
    valid_street = ""
    valid_city = ""
    valid_zip_code = ""'''
    name = ""
    street = ""
    city = ""
    zip_code = ""

    existing_company = Companies.query.filter_by(name=name).first()
        
    '''if not existing_company:
        if request.method == 'POST':
            name = request.form['name']
            street = request.form['street']
            city = request.form['city']
            zip_code = request.form['zip_code']

            if len(name) < 2:
                valid_name = "Not a Valid Company Name"
                
            if len(street) < 1:
                valid_street = "Not a Valid Street Name"

            if len(city) < 2:
                    valid_city ="Not a Valid City"
            if len(zip_code) <= 4:
                    valid_zip_code = "Not a valid zip code"
    else:
        valid_name = "Company Already Exists" '''


    if name=="" and street=="" and city=="" and zip_code=="":
        new_companies = Companies(name = name, street = street, city = city, zip_code = zip_code)
        db.session.add(new_companies)
        db.session.commit()
        return render_template('/companies.html',name = name, city = city, street = street, zip_code=zip_code)
    else:   
        return "Not working"
    return render_template("add_companies.html")    

@app.route("/companies")
def companies():
    return render_template("/companies.html")


    
if __name__ == '__main__':
    app.run()
