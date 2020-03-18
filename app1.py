from flask import Flask, render_template, url_for, redirect, flash, request ,session
import os
import secrets
import pypyodbc
from forms import LoginForm,ProfileForm,AdminLoginForm,ForgotForm,ResetForm,ResetpassForm,SearchForm,SkillsForm,ProjectForm
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
global mng

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            name1 = form.name.data
            pass1 = form.password.data
            if name1 == "admin" and pass1 == "admin":
                session['user'] = True
                return redirect(url_for('adminprofile'))
            else:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('adminlogin'))
    return render_template('adminlogin.html', form=form)


@app.route('/',methods=['GET', 'POST'])
@app.route('/login',methods=['GET', 'POST'])
def login():
    global a,results1,mng
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            cursor = connection1.cursor()
            select = "SELECT * FROM signin WHERE empid=?"
            name1 = form.name.data
            global a,mng
            a=name1
            pass1 = form.password.data
            cursor.execute(select, [name1])
            results = cursor.fetchone()
            mng = results[2]
            print(mng)
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


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            result = request.form
            global a ,mng,results1
            cursor = connection1.cursor()
            select = "SELECT * FROM profile WHERE empid='"+ a +"'"
            cursor.execute(select)
            results = cursor.fetchone()
            print(results)
            if results == None:
                cursor = connection1.cursor()
                insert = ("INSERT INTO profile (fname,lname,email,experience,practice,ejoindate,currentpro,location,gender,ques,ans,empid) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)")
                values = list(result.values())
                values = [values[1], values[2], values[3], values[8], values[9], values[5], values[6], values[7],values[4],values[10],values[11],a]
                cursor.execute(insert, values)
                connection1.commit()
            cursor.execute("SELECT * FROM profile WHERE empid='"+ a +"'")
            results1=cursor.fetchone()
            return redirect(url_for('profile1'))
    return render_template('profile.html',form=form,mng=mng)


@app.route('/profile1', methods=['GET', 'POST'])
def profile1():
    if request.method == 'POST':
        global results1
        fname=request.form['fname1']
        lname=request.form['lname1']
        email=request.form['email1']
        exp = request.form['exp1']
        select12 = request.form['select1']
        date = request.form['date1']
        select21 = request.form['select2']
        select31 = request.form['select3']
        select41 = request.form['select4']
        cursor = connection1.cursor()
        update = ("UPDATE profile SET fname=?,lname=?,email=?,experience=?,practice=?,ejoindate=?,currentpro=?,location=?,gender=? where empid='"+a+"'")
        values = [fname,lname,email,exp,select12,date,select21,select31,select41]
        cursor.execute(update, values)
        connection1.commit()
        select1 = "select * from profile where empid ='" + a + "'"
        cursor.execute(select1)
        results1 = cursor.fetchone()
        return redirect(url_for('profile1'))
    return render_template('profile1.html',results1=results1,mng=mng)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',mng=mng)


@app.route('/dashboard1')
def dashboard1():
    return render_template('dashboard1.html',mng=mng)



@app.route('/forgotpassword',methods=['POST','GET'])
def forgotpassword():
    form = ForgotForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            cursor = connection1.cursor()
            empid1 = form.empid.data
            global a
            a = empid1
            ques1 = form.select1.data
            ans1 = form.ans.data
            select = "SELECT ques,ans FROM profile where empid='"+empid1+"'"
            cursor.execute(select)
            results = cursor.fetchone()
            if results is not None:
                ans = results[1]
                ques = results[0]
                if  ans == ans1 and ques1 == ques:
                    return redirect(url_for("reset"))
                else:
                    flash('Please enter correct answer to question', 'danger')
            else:
                flash('Please enter correct Employee ID', 'danger')
    return render_template('forgotpassword.html', form=form)



@app.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ResetForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            global a
            results=request.form
            values=list(results.values())
            if values[1] == values[2]:
                cursor = connection1.cursor()
                update = ("UPDATE signin SET password =? where  empid ='"+a+"'")
                values=[values[1]]
                cursor.execute(update, values)
                connection1.commit()
                return redirect(url_for('login'))
            else:
                flash('Please enter same password in both fields', 'danger')
    return render_template('reset.html', form=form)


global data;


@app.route('/skills',methods=['POST','GET'])
def skills():
    cursor = connection1.cursor()
    cursor.execute("select skill,rating from skills where empid='" + a + "'")
    global data
    data = cursor.fetchall()
    form=SkillsForm()
    return render_template('skills.html',value=data,form=form,mng=mng)


@app.route('/add',methods=['POST'])
def add():
    cursor = connection1.cursor()
    cursor.execute("select skill,rating from skills where empid='" + a + "'")
    global data
    data = cursor.fetchall()
    form = SkillsForm()
    if form.validate_on_submit():
        if request.method == "POST":
            result = request.form
            cursor = connection1.cursor()
            insert = ("INSERT INTO skills "
                      "(empid,skill,rating)"
                      "VALUES(?,?,?)")
            values = list(result.values())
            values = [a,values[1], values[2]]
            cursor.execute(insert, values)
            connection1.commit()
            cursor.execute("select skill,rating from skills where empid='" + a + "'")
            data = cursor.fetchall()
            form.select1.data = ""
            form.select2.data = ""
    return render_template('skills.html',form=form,value=data,mng=mng)


@app.route('/edit', methods=['POST'])
def edit():
    if request.method == "POST":
        cursor = connection1.cursor()
        x1 = request.form['x']
        if x1!="Edit":
            rate1 = request.form['rate' + x1]
            sk = data[int(x1) - 1][0]
            update = "UPDATE skills SET rating=? where empid='" + a + "' and skill = '" + sk + "'"
            values = [rate1]
            cursor.execute(update, values)
            connection1.commit()
    return render_template('skills.html', value=data, mng=mng)




@app.route('/skills1')
def skills1():
    cursor = connection1.cursor()
    cursor.execute("with cte as(select empid from signin where mngid='"+ a +"')"
    "select s.empid,p.fname+p.lname from cte s inner join profile p on p.empid=s.empid")
    value = cursor.fetchall()
    return render_template('skills1.html',value=value,mng=mng)


@app.route('/projects',methods=['POST','GET'])
def projects():
    cursor = connection1.cursor()
    cursor.execute("select project,client,mngid from projects where empid='" + a + "'")
    data = cursor.fetchall()
    form = ProjectForm()
    if form.validate_on_submit():
        if request.method == "POST":
            result = request.form
            cursor = connection1.cursor()
            insert = ("INSERT INTO projects "
                      "(empid,project,client,mngid)"
                      "VALUES(?,?,?,?)")
            values = list(result.values())
            values = [ a,values[1], values[2],values[3]]
            cursor.execute(insert, values)
            connection1.commit()
            cursor.execute("select project,client,mngid from projects where empid='" + a + "'")
            data = cursor.fetchall()
            form.clients1.data = ""
            form.manager1.data = ""
            form.projects.data = ""
            return render_template('projects.html', value=data, form=form)
    return render_template('projects.html', form=form, value=data,mng=mng)


@app.route('/search',methods=['GET','POST'])
def search():
    form=SearchForm()
    if form.validate_on_submit():
        if request.method=='POST':
            values=list(request.form.values())
            cursor=connection1.cursor()
            select=("with cte as (select p.*,pr.client,s.rating,s.skill from profile p inner join projects pr on p.empid=pr.empid inner join skills s on s.empid=pr.empid)"
            "select * from cte where skill like ? and client like ? and rating like ? and location like ? and practice like ? and experience like ? and currentpro like ?")
            values=[values[1],values[2],values[4],values[6],values[5],values[3],values[7]]
            cursor.execute(select,values)
            result5=cursor.fetchall()
            return render_template('search.html',result5=result5,form=form)
    return render_template('search.html',form=form)


@app.route('/resetpass',methods=['POST','GET'])
def resetpass():
    form = ResetpassForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            global a
            results = request.form
            values = list(results.values())
            cursor = connection1.cursor()
            select = "SELECT password FROM signin where empid='" + a + "'"
            cursor.execute(select)
            results2=cursor.fetchone()
            if values[1]==results2[0]:
                if values[2] == values[3]:
                    cursor = connection1.cursor()
                    update = ("UPDATE signin SET password =? where  empid ='" + a + "'")
                    values = [values[2]]
                    cursor.execute(update, values)
                    connection1.commit()
                    flash('Updated succesfully','success')
                    return redirect(url_for('resetpass'))
                else:
                    flash('Please enter same password in both fields', 'danger')
            else:
                flash('Incorrect Password')
    return render_template('resetpass.html', form=form,mng=mng)


@app.route('/rate',methods=['POST','GET'])
def rate():
    var=request.args.get('var',None)
    cursor=connection1.cursor()
    cursor.execute("select sk.skill from profile p inner join signin s on p.empid=s.empid inner join skills sk on p.empid=sk.empid where s.mngid='"+ a +"' and p.empid='"+ var +"'")
    l = cursor.fetchall()
    t = [i[0] for i in l]
    print(t)
    if request.method == 'POST':
        x1 = request.form['y']
        rate1 = request.form['rate'+x1]
        sk = t[int(x1)-1]
        print(rate1)
        print(x1)
        cursor = connection1.cursor()
        if rate1 != "None":
            update = "UPDATE skills SET mngrat=? where empid='" + var + "' and skill = '" + sk + "'"
            values = [rate1]
            cursor.execute(update, values)
            connection1.commit()
    return render_template('rate.html',t=t,mng=mng,actions=actions)


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))


@app.route('/adminprofile')
def adminprofile():
    return render_template('adminprofile.html')


@app.route('/adduser')
def adduser():
    return render_template('adduser.html')


if __name__ == '__main__':
    app.run(debug=True)
