from flask import Flask, request, redirect
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask (__name__)
app.config['DEBUG'] = True

@app.route("/")
def home():
    template = jinja_env.get_template("index.html")
    return template.render()

@app.route("/signup")
def index():
    template = jinja_env.get_template('signup.html')
    return template.render()

def length(parameter):
    if len(parameter)> 2 and len(parameter)<21:
        return True
    else:
        return False

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

@app.route('/validation', methods=['POST'])
def validation():   

    username = request.form['username']
    password = request.form['password']
    verifypassword = request.form['verifypassword']
    email = request.form['email']
 
    if length(username) and no_space(username):
        valid_username = ""
    else:
        valid_username = "Not a valid username"
    
    if length(password) and no_space(password) and password == verifypassword:
        valid_password = ""
    else: 
        valid_password = "Not a valid password"
        
    if length(email) and symbol(email) and no_space(email) or email == "":
        valid_email = ""
    else:
        valid_email = "Not a valid email"

    if valid_username=="" and valid_password=="" and valid_email=="":
        return redirect('/welcome?username='+username)
    else:
        template = jinja_env.get_template('index.html')
        return template.render(username=username, email=email, valid_username=valid_username, valid_password=valid_password, valid_email = valid_email)
        
@app.route('/welcome')
def welcome():   
    template = jinja_env.get_template('welcome.html')
    username=request.args.get('username')
    return template.render(username = username)

app.run()