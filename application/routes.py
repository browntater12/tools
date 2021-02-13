from flask import render_template, request, flash, redirect, session
from application import app
from wtforms import Form, TextField, PasswordField, BooleanField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
import csv

username = False
################## OOP Attempt
class page:
    def __init__(self, department, location):
        self.department = department
        self.location = []
        self.location += location
        self.departmentURL = department.lower().replace(" ", "")
        self.locationURL = location.lower().replace(" ", "")
        function =  self.departmentURL

    def removeLocation(self, location):
        self.location.remove(location)
        
    def addLocation(self, location):
        self.location += [location]
    
    def changeLocation(self, location, newLocation):
        self.location = newLocation
    
    @app.route(f'/taco/')
    def function():
        return render_template(department + ".html" , function=True, department=self.department)
 #########################   

'''
pages = {'Direct Mail in Repair': ['TLC', 'SPG', 'AUS', 'UBIF'], 'In Store Repair': ['AT&T', 'UBIF', 'SPR-TMO'], 'Remote Repair': ['UBIF', '3P']}
keys =  list(pages.keys())
length = len(keys)
urls = [x.lower().replace(" ","") for x in keys]
'''

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])
    
'''
@app.route('/<function>')
def direct(function):
    file = open('test.csv', 'r')
    reader = csv.reader(file)
    if function == "jeff":
        return "<h1>Hello</h1>"
    elif function == "direct":
        return render_template("direct.html", direct=True, reader=reader)
'''
@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        result = request.form
        if result['password'] == 'potato':
            session['username'] = 'admin'
            username = session['username']
        else:
            flash("Incorrect Password.") 
            session.pop('username', None)        
    return render_template("home.html")

@app.route('/direct/', methods=['POST', 'GET'])
def direct():
    file = open('test.csv', 'r')
    reader = csv.reader(file)
    if request.method == 'POST':
        result = request.form
        if result['password'] == 'potato':
            session['username'] = 'admin'
            username = session['username']
            return render_template("direct.html", username=username, reader=reader, direct=True)
        else:
            flash("Incorrect Password.")
    return render_template("direct.html", reader=reader, direct=True)

@app.route('/inStore/', methods=['POST', 'GET'])
def inStore():
    if request.method == 'POST':
        result = request.form
        if result['password'] == 'potato':
            session['username'] = 'admin'
        else:
            flash("Incorrect Password.")
    return render_template("inStore.html", inStore=True)

@app.route('/remote/', methods=['POST', 'GET'])
def remote():
    if request.method == 'POST':
        result = request.form
        if result['password'] == 'potato':
            session['username'] = 'admin'
        else:
            flash("Incorrect Password.")
    return render_template("remote.html", remote=True)








@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))
                
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))







