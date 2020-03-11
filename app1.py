from flask import Flask, render_template, url_for, redirect, flash, request ,session
import os
import secrets
import pypyodbc
from forms import LoginForm,AdminLoginForm,ProfileForm,Profile1Form
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = b'fr\xb2\xa8\xfa\xbf{\x95\x0b0}M'
bcrypt=Bcrypt(app)
connection1 = pypyodbc.connect(
    "Driver={SQL Server};"
    "Server=LAPTOP-PB290PQU;"
    "Database=project;"
    "Trusted_Connection=yes;"
)



@app.route('/',methods=['GET', 'POST'])
@app.route('/login',methods=['GET', 'POST'])
def login():
    global a
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            cursor = connection1.cursor()
            select = "SELECT empid,password FROM signin WHERE empid=?"
            name1 = form.name.data
            global a,results1
            a=name1
            pass1 = form.password.data
            cursor.execute(select, [name1])
            results = cursor.fetchone()
            if results !=None:
                password = results[1]
                if name1 in results and password == pass1:
                    session['user'] = True
                    select1 = "select * from profile where empid ='"+name1+"'"
                    cursor.execute(select1)
                    results1 = cursor.fetchone()
                    if results1!=None:
                        return redirect(url_for('profile1'))
                    else:
                        return redirect(url_for('profile'))
            else:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            name1 = form.name.data
            pass1 = form.password.data
            if name1 == "admin" and pass1 == "admin":
                return render_template('adminprofile.html')
            else:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('adminlogin'))
    return render_template('adminlogin.html', form=form)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')




@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')


@app.route('/skills')
def skills():
    return render_template('skills.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/resetpass')
def resetpass():
    return render_template('resetpass.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            result = request.form
            global a
            cursor = connection1.cursor()
            select = "SELECT * FROM profile WHERE empid='"+ a +"'"
            cursor.execute(select)
            results = cursor.fetchone()
            print(results)
            if results == None:
                cursor = connection1.cursor()
                insert = ("INSERT INTO profile (fname,lname,email,experience,practice,ejoindate,currentpro,location,gender,empid) VALUES(?,?,?,?,?,?,?,?,?,?)")
                values = list(result.values())
                values = [values[1], values[2], values[3], values[4],values[5],values[6],values[7],values[8],values[9],a]
                cursor.execute(insert, values)
                connection1.commit()
    return render_template('profile.html',form=form)

#@app.route('/', methods=['GET', 'POST'])
@app.route('/profile1', methods=['GET', 'POST'])
def profile1():
    form = Profile1Form()
    if form.validate_on_submit():
        if request.method == 'POST':
            result=request.form
            cursor = connection1.cursor()
            update = ("UPDATE profile SET fname=?,lname=?,email=?,experience=?,practice=?,ejoindate=?,currentpro=?,location=?,gender=? where empid='hk'")
            values=list(result.values())
            values = [values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9]]
            cursor.execute(update, values)
            connection1.commit()
    return render_template('profile1.html',form=form,)






@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
