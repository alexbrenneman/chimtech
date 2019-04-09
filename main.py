from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

error = False

app = Flask (__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chimtech:chimtech@localhost:8889/chimtech'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'f8wv3w2f>v9j4sEuhcNYydAGMzzZJgkGgyHE9gUqaJcCk^f*^o7fQyBT%XtTvcYM'


# Main landing page (home page)----------------------------------------------------------------------
@app.route("/")
def index():
    error = False
    return render_template("index.html")


# This is setup for the User table in the MySQL database---------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(150))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zipcode = db.Column(db.Integer)
    appliance = db.Column(db.String(100))



# Check for proper symbols for email validation-------------------------------------------------------
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
     

# This is the signup method ------------------------------------------------------------------------
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    valid_username  = ''
    valid_password = ''
    username = ''
    email = ''
    valid_email = ''
    address = ''
    city = ''
    state = ''
    zipcode = ''
    appliance = ''
    valid_address = ''
    valid_city = ''
    valid_state = ''
    valid_zipcode = ''
    valid_appliance = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        appliance = request.form['appliance']
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

            if len(address) < 1:
                valid_address = "Not a valid address"

            if len(city) < 1:
                valid_city = "Not a valid city"

            if len(state) < 1:
                valid_state = "Not a valid state"

            if len(zipcode) <= 4:
                valid_zipcode = "Not a valid zip code"

            if len(appliance) < 1:
                valid_appliance = "Not a valid appliance"
        else:
            valid_username = 'Duplicate user'

        

        if valid_username=="" and valid_password=="" and valid_email=="" and valid_address=="" and valid_city=="" and valid_state=="" and valid_zipcode=="" and valid_appliance=="":
            new_user = User(username = username, password = password, email = email, address = address, city = city, state = state, zipcode = zipcode, appliance = appliance)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return render_template('/welcome.html',username = username, email = email, address = address, city = city, state = state, zipcode = zipcode, appliance = appliance )
                
        

    return render_template('signup.html', valid_username=valid_username, username=username , valid_password=valid_password , email=email, address = address, city = city, state = state, zipcode = zipcode, appliance = appliance, valid_address = valid_address, valid_city = valid_city, valid_state = valid_state, valid_zipcode = valid_zipcode, valid_appliance = valid_appliance)



# This is the user profile page and how the user will get back to their personalized page--------------------------------------------------
@app.route('/profile', methods=['POST','GET'])
def profile():
    if "username" in session:
        user = User.query.filter_by(username=session["username"]).first()
    else:
        return render_template("profile.html")
        
    return render_template(("/profile.html"),user=user)


# Welcome landing page after user either signs up or logs in------------------------------------------------------
@app.route('/welcome', methods=['POST', 'GET'])
def welcome():   
    username = request.form.get('username')
    email = request.form.get('email')
    return render_template(('welcome.html'),username = username, email = email)


# This is the login method----------------------------------------------------------------------------------------
@app.route('/login', methods= ['GET','POST'])
def login():
    error = False
    valid_username  = 'Not valid username'
    valid_password = 'Not valid password'
    username = ''
    email=''
    address = ''
    city = ''
    state = ''
    zipcode = ''
    appliance = ''

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
                return render_template('/welcome.html', username = username, email = user.email,  address = user.address, city = user.city, state = user.state, zipcode = user.zipcode, appliance = user.appliance)
        
        
           
    return render_template('login.html', valid_username=valid_username, valid_password=valid_password, error=False)


# Logout deletes the current session--------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')





# This is setup for the Companies table in the MySQL database--------------------------------------------- 
class Companies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    street = db.Column(db.String(120))
    city = db.Column(db.String(120))
    zip_code = db.Column(db.Integer)
    phone = db.Column(db.String(100))
    site = db.Column(db.String(120))
    rating = db.Column(db.Integer)


# This is how users add new companies to our database and then show them at '/companies'---------------------
@app.route('/add_companies', methods = ['POST'])
def add_companies():
    valid_name = ""
    valid_street = ""
    valid_city = ""
    valid_zip_code = ""
    valid_phone = ""
    valid_site = ""
    name = ""
    street = ""
    city = ""
    zip_code = ""
    phone = ""
    site = ""

    existing_company = Companies.query.filter_by(name=name).first()
        
    name = request.form['name']
    street = request.form['street']
    city = request.form['city']
    zip_code = request.form['zip_code']
    phone = request.form['phone']
    site = request.form['site']


    if len(name) < 2:
        valid_name = "Not a Valid Company Name"
        
    if len(street) < 1:
        valid_street = "Not a Valid Street Name"

    if len(city) < 2:
            valid_city ="Not a Valid City"
    
    if len(zip_code) <= 4:
        valid_zip_code = "Not a valid zip code"

    if len(phone) < 10:
        valid_phone = "Not a valid phone number"

    if len(site) < 2:
        valid_site = "Not a valid website"


    if valid_name=="" and valid_street=="" and valid_city=="" and valid_zip_code=="" and valid_phone == "" and valid_site == "":
        new_companies = Companies(name = name, street = street, city = city, zip_code = zip_code, phone=phone, site=site, rating=0)
        db.session.add(new_companies)
        db.session.commit()
        return redirect('/companies')
    else:   
        return render_template("add_companies.html", valid_city =valid_city, valid_name=valid_name, valid_street=valid_street, valid_zip_code=valid_zip_code, valid_phone=valid_phone, valid_site=valid_site)


# This method is used to show the add_companies.html template------------------------------------------------
@app.route('/add_companies', methods = ['GET'])
def add_temp():
    return render_template("add_companies.html")


# This method makes it a requirement to be logged in before you can see the company list or like companies------
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


# This method shows our current company list along with the user rating system------------------------------------
@app.route("/companies", methods=["POST","GET"])
def companies():
    rating =""
    com = ""
    name = ""
    companies = Companies.query.all()
    if request.method == 'POST':
        rating = request.form['rating']
        com = request.form["com"]
        user = Companies.query.filter_by(name = com).first()
        user.rating += 1
        db.session.commit()
    else:
        return render_template('/companies.html', companies=companies)
        
    return render_template("/companies.html", companies=companies, rating=rating)


    
if __name__ == '__main__':
    app.run()
