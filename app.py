from flask import Flask, render_template, url_for, redirect, flash, request, session
import os
import secrets
import pypyodbc
from forms import LoginForm,ProfileForm,AdminLoginForm,ForgotForm,ResetForm,ResetpassForm,SearchForm,SkillsForm,DeleteuserForm,SkillForm
from flask_bcrypt import Bcrypt
import re


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
    global a, results1, mng
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            cursor = connection1.cursor()
            select = "SELECT * FROM signin WHERE empid=?"
            name1 = form.name.data
            global a,mng
            a=name1
            # pass1 = form.password.data
            cursor.execute(select, [name1])
            results = cursor.fetchone()


            if results !=None:
                mng = results[2]
                password = results[1]
                if name1 in results and bcrypt.check_password_hash(password, form.password.data):
                    session['user'] = True
                    select1 = "select * from profile where empid ='"+name1+"'"
                    cursor.execute(select1)
                    results1 = cursor.fetchone()
                    if results1!=None:
                        if mng != None:
                            return redirect(url_for('dashboard'))
                        else:
                            return redirect(url_for('dashboard1'))
                    else:
                        return redirect(url_for('profile'))
                else:
                    flash('Invalid username or password', 'danger')
                    return redirect(url_for('login'))
            else:
                flash("Employee doesn't exists",'danger')
                return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/firstreset', methods=['POST', 'GET'])
def firstreset():
    form = ResetpassForm()
    form2 = ProfileForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            global a
            results = request.form
            values = list(results.values())
            cursor = connection1.cursor()
            select = "SELECT password FROM signin where empid='" + a + "'"
            cursor.execute(select)
            results2=cursor.fetchone()
            if bcrypt.check_password_hash(results2[0], values[1]):

                if values[2] == values[3]:
                    if bcrypt.check_password_hash(results2[0], values[2]):
                        flash('Old and New passwords must be different','danger')

                    else:
                        cursor = connection1.cursor()
                        update = ("UPDATE signin SET password =? where  empid ='" + a + "'")
                        hashed_password = bcrypt.generate_password_hash(values[2]).decode('utf-8')
                        values = [hashed_password]

                        cursor.execute(update, values)
                        connection1.commit()
                        return redirect(url_for('afterreset'))
                else:
                    flash('Please enter same password in both fields', 'danger')
            else:
                flash('Incorrect Password','danger')
    return render_template('profile.html', form=form,form2=form2, mng=mng,open=True)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form2 = ProfileForm()
    form = ResetpassForm()
    return render_template('profile.html',form2=form2,form=form,mng=mng,open=True)


@app.route('/afterreset', methods=['GET', 'POST'])
def afterreset():
    form2 = ProfileForm()
    form = ResetpassForm()
    return render_template('profile.html',form2=form2,form=form,mng=mng,open=False)


@app.route('/firstfill', methods=['GET', 'POST'])
def firstfill():
    form2 = ProfileForm()
    form = ResetpassForm()
    if form2.validate_on_submit():
        if request.method == 'POST':
            result = request.form
            values = list(result.values())
            addresstoverify = values[3]
            s1=values[1]
            s2 = values[2]
            match2=re.match("^[A-z][A-z|\.|\s]+$",s1)
            match3 = re.match("^[A-z][A-z|\.|\s]+$", s2)
            match1 = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@enquero.com$', addresstoverify)
            if match1 == None:
                flash('Incorrect email address','danger')
                return redirect(url_for('firstfill'))
            elif match2 == None:
                flash('Incorrect First Name', 'danger')
                return redirect(url_for('firstfill'))
            elif match3==None:
                flash('Incorrect Last Name', 'danger')
                return redirect(url_for('firstfill'))

            else:
                global a ,mng,results1
                cursor = connection1.cursor()
                select = ("SELECT * FROM profile WHERE empid='"+ a +"'")
                cursor.execute(select)
                results = cursor.fetchone()

                if results == None:
                    cursor = connection1.cursor()
                    insert = ("INSERT INTO profile (fname,lname,email,experience,practice,ejoindate,currentpro,location,gender,ques,ans,empid) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)")

                    values = [values[1], values[2], values[3], values[8], values[9], values[5], values[6], values[7],values[4],values[10],values[11],a]
                    cursor.execute(insert, values)
                    connection1.commit()
                cursor.execute("SELECT * FROM profile WHERE empid='"+ a +"'")
                results1 = cursor.fetchone()
                if mng != None:
                    return redirect(url_for('skills'))
                else:
                    return redirect(url_for('skills1'))
    return render_template('profile.html',form2=form2,form=form, mng=mng, open=False)


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
        values = [fname, lname, email, exp, select12, date, select21, select31, select41]
        cursor.execute(update, values)
        connection1.commit()
        select1 = "select * from profile where empid ='" + a + "'"
        cursor.execute(select1)
        results1 = cursor.fetchone()
        flash('Updated Successfully', 'success')
        return redirect(url_for('profile1'))
    return render_template('profile1.html', results1=results1, mng=mng)


@app.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    cursor = connection1.cursor()
    global a
    cursor.execute("select skill,rating from skills where empid ='" + a + "' ")
    l1 = cursor.fetchall()
    if l1 != []:
        d1= {}
        for i in l1:
            d1[i[0]] = i[1]
        # d1 = {k: d1[k] for k in sorted(d1, key=d1.get)}
        data1 = {'Skill': 'Rating'}

        data1.update(d1)
        cursor.execute("SELECT round(avg(cast(rating as float)),2) from skills where empid ='" + a + "'  group by empid")
        bb = cursor.fetchone()  # data from database
        rating = bb[0]
        cursor = connection1.cursor()
        cursor.execute("with cte as(select max(rating) as m,skill from skills group by skill) select s.skill,s.rating,c.m from skills s inner join cte c on s.skill=c.skill where empid='" + a + "' ")
        l3 = cursor.fetchall()  # data from database
        # d = {}
        cursor.execute("select distinct count(skill) from skills where empid='" + a + "' ")
        j3 = cursor.fetchall()
        k3 = j3[0][0]
        n = [*range(k3)]
        t3 = []
        for i in l3:
            t3.append(list(i[0:]))
        m3 = sorted(t3, key=lambda x: x[1])

        data3 = m3
        cursor = connection1.cursor()
        cursor.execute("with cte as(select * from skills where empid=" + a + ")select d.empid,p.fname,d.skill from (select a.empid,b.skill from cte b inner join skills a on a.skill=b.skill where a.empid!=b.empid) d inner join profile p on p.empid=d.empid")

        l = cursor.fetchall()
        cursor.execute("select empid,skill from skills where empid='" + a + "' ")
        b = cursor.fetchall()
        b1 = len(b)
        # print(l)
        d = {}
        for i in l:
            j = i[0]
            if j in d:
                L = d[j]
                L.append(i[2])
                d[j] = L
            else:
                L = []
                L.extend(i[1:])
                d[j] = L
        # print(d)

        d1 = {}
        for key, value in d.items():
            if len(value) == b1+1:
                d1[key] = value

        sk = [[i, j[0]] for i, j in d1.items()]

        return render_template('dashboard.html', mng=mng, rating=rating, data1=data1, data3=data3, n=n, sk=sk)
    else:
        flash("No skills added yet..Please enter your skills", 'warning')
        return redirect(url_for('skills'))


@app.route('/dashboard1')
def dashboard1():
    cursor = connection1.cursor()
    cursor.execute("select round( (avg(cast(rating as float))+avg(cast(isnull(mngrat,rating) as float)))/2 ,2) from skills where empid in (select empid from signin where mngid='"+a+"')")
    h = cursor.fetchone()  # data from database
    rat = h[0]
    cursor = connection1.cursor()
    cursor.execute("select skill,round( (avg(cast(rating as float))+avg(cast(isnull(mngrat,rating) as float)))/2 ,2) from skills  where empid in (select empid from signin where mngid='"+a +"') group by skill")
    l5 = cursor.fetchall()  # data from database
    d5 = {}
    for i in l5:
        d5[i[0]] = i[1]
    # d5 = {k: d5[k] for k in sorted(d5, key=d5.get)}
    data5 = {'Skill': 'Rating'}
    data5.update(d5)

    return render_template('dashboard1.html',mng=mng,rat=rat,data5=data5)


@app.route('/forgotpassword',methods=['POST', 'GET'])
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
            values = list(results.values())
            if values[1] == values[2]:
                cursor = connection1.cursor()
                update = ("UPDATE signin SET password =? where  empid ='"+a+"'")
                hashed_password = bcrypt.generate_password_hash(values[1]).decode('utf-8')
                values=[hashed_password]
                cursor.execute(update, values)
                connection1.commit()
                return redirect(url_for('login'))
            else:
                flash('Please enter same password in both fields', 'danger')
    return render_template('reset.html', form=form)


global data2


@app.route('/skills',methods=['POST','GET'])
def skills():
    cursor = connection1.cursor()
    cursor.execute("select skill,rating from skills where empid='" + a + "'")
    global data2
    data2 = cursor.fetchall()

    form = SkillsForm()
    return render_template('skills.html', value=data2, form=form, mng=mng)


@app.route('/check', methods=['POST','GET'])
def check():
    global data2

    form = SkillsForm()
    if len(data2) == 0:
        flash('Skills not yet added', 'warning')
    else:
        return redirect(url_for('edit'))
    return render_template('skills.html', form=form, value=data2, mng=mng)


@app.route('/add', methods=['POST','GET'])
def add():
    cursor = connection1.cursor()
    cursor.execute("select skill,rating from skills where empid='" + a + "'")
    global data2
    data2 = cursor.fetchall()
    cursor.execute("select skill from skills where empid='" + a + "'")
    db = cursor.fetchall()
    existing = [i[0] for i in db]

    form = SkillsForm()
    if form.validate_on_submit():
        if request.method == "POST":
            result = request.form
            cursor = connection1.cursor()
            values = list(result.values())

            if values[1] not in existing:
                insert = ("INSERT INTO skills "
                          "(empid,skill,rating)"
                          "VALUES(?,?,?)")

                values = [a, values[1], values[2]]
                cursor.execute(insert, values)
                connection1.commit()
                cursor.execute("select skill,rating from skills where empid='" + a + "'")
                data2 = cursor.fetchall()
                form.select1.data = ""
                form.select2.data = ""
                flash('Skill added successfully', 'success')
            else:
                flash('This skill is already added', 'danger')
    return render_template('skills.html', form=form, value=data2, mng=mng)


@app.route('/edit',methods=['POST', 'GET'])
def edit():
    if request.method == "POST":
        global data2
        n=len(data2)
        rates=[]
        for i in range(1,n+1):
            rates.append(request.form['rate'+str(i)])
        cursor = connection1.cursor()
        for i in range(0, n):
            update = "UPDATE skills set rating=? where empid='" + a + "' and skill = '" + data2[i][0] + "'"
            values=[rates[i]]
            cursor.execute(update,values)
        connection1.commit()
        # flash('Ratings Updated Succesfully','success')
        return redirect(url_for('add'))
    return render_template('edit.html', value=data2, mng=mng)


@app.route('/delete', methods=['POST','GET'])
def delete():
    form = SkillsForm()
    global data2
    if request.method == "POST":
        cursor = connection1.cursor()
        x1 = request.form['dlt']

        sk = data2[int(x1) - 1][0]
        update = "DELETE from skills where empid='" + a + "' and skill = '" + sk + "'"
        cursor.execute(update)
        connection1.commit()
        cursor.execute("select skill,rating from skills where empid='" + a + "'")
        data2 = cursor.fetchall()
        flash('Skill deleted succesfully', 'success')
    return render_template('skills.html', value=data2, form=form, mng=mng)


@app.route('/skills1')
def skills1():
    cursor = connection1.cursor()
    cursor.execute("with cte as(select empid from signin where mngid='"+ a +"')"
    "select s.empid,p.fname+p.lname from cte s inner join profile p on p.empid=s.empid")
    value = cursor.fetchall()
    return render_template('skills1.html', value=value, mng=mng)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form=SearchForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            values=list(request.form.values())
            if values[1]=='current':
                query="select p.*,skill,round( (cast(rating as float)+isnull(cast(mngrat as float),cast(rating as float)))/2,2) as rating from profile p inner join skills s on s.empid=p.empid where skill like ? and round( (cast(rating as float)+isnull(cast(mngrat as float),cast(rating as float)))/2,2) >= ? and location like ? and practice like ? and experience  like ? and currentpro like ?"
                cursor = connection1.cursor()
                select = (query)
                values = [values[2], values[3], values[7], values[6], values[4], values[5]]
                cursor.execute(select, values)
                result5 = cursor.fetchall()
            elif values[1] == 'old':
                query = "select p.*,skill,round( (cast(rating as float)+isnull(cast(mngrat as float),cast(rating as float)))/2,2) as rating from old_profile p inner join old_skills s on s.empid=p.empid where skill like ? and round( (cast(rating as float)+isnull(cast(mngrat as float),cast(rating as float)))/2,2) >= ? and location like ? and practice like ? and experience  like ? and currentpro like ?"

                cursor = connection1.cursor()
                select = (query)
                values = [values[2], values[3], values[7], values[6], values[4], values[5]]
                cursor.execute(select, values)
                result5 = cursor.fetchall()
            else:
                values = [values[2], values[3], values[7], values[6], values[4], values[5]]
                query = "select p.*,skill,round( (cast(rating as float)+isnull(cast(mngrat as float),cast(rating as float)))/2,2) as rating from profile p inner join skills s on s.empid=p.empid where skill like ? and round( (cast(rating as float)+isnull(cast(mngrat as float),cast(rating as float)))/2,2) >= ? and location like ? and practice like ? and experience  like ? and currentpro like ?"

                cursor = connection1.cursor()
                select = (query)

                cursor.execute(select, values)
                current = cursor.fetchall()
                query = "select p.*,skill,round( (cast(rating as float)+isnull(cast(mngrat as float),cast(rating as float)))/2,2) as rating from old_profile p inner join old_skills s on s.empid=p.empid where skill like ? and round( (cast(rating as float)+isnull(cast(mngrat as float),cast(rating as float)))/2,2) >= ? and location like ? and practice like ? and experience  like ? and currentpro like ?"

                cursor = connection1.cursor()
                select = query

                cursor.execute(select, values)
                old = cursor.fetchall()
                current.extend(old)
                result5=current

            return render_template('search.html',result5=result5,form=form,tablet=True)
    return render_template('search.html',form=form,tablet=False)


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
            if bcrypt.check_password_hash(results2[0], values[1]):

                if values[2] == values[3]:
                    if bcrypt.check_password_hash(results2[0], values[2]):
                        flash('Old and New Passwords must be different','danger')
                        return redirect(url_for('resetpass'))
                    else:
                        cursor = connection1.cursor()
                        update = ("UPDATE signin SET password =? where  empid ='" + a + "'")
                        hashed_password = bcrypt.generate_password_hash(values[2]).decode('utf-8')
                        values = [hashed_password]

                        cursor.execute(update, values)
                        connection1.commit()
                        flash('Updated succesfully','success')
                        return redirect(url_for('resetpass'))
                else:
                    flash('Please enter same password in both fields', 'danger')
            else:
                flash('Incorrect Password','danger')
    return render_template('resetpass.html', form=form,mng=mng)


@app.route('/rate',methods=['POST','GET'])
def rate():
    var=request.args.get('var',None)
    cursor=connection1.cursor()
    cursor.execute("select sk.skill,sk.mngrat,sk.rating from profile p inner join signin s on p.empid=s.empid inner join skills sk on p.empid=sk.empid where s.mngid='"+ a +"' and p.empid='"+ var +"'")
    l = cursor.fetchall()
    print(l)
    t = [i[0] for i in l]
    det = [i for i in l]

    if request.method == 'POST':
        n=len(t)
        mngrates=[]
        for i in range(1,n+1):
            mngrates.append(request.form['rate'+str(i)])
        for i in range(0,n):
            if(mngrates[i]!="None"):
                update = "UPDATE skills SET mngrat=? where empid='" + var + "' and skill = '" + t[i] + "'"
                values = [mngrates[i]]
                cursor.execute(update, values)
        connection1.commit()
        cursor = connection1.cursor()
        cursor.execute("select sk.skill,sk.mngrat,sk.rating from profile p inner join signin s on p.empid=s.empid inner join skills sk on p.empid=sk.empid where s.mngid='" + a + "' and p.empid='" + var + "'")
        l = cursor.fetchall()
        det = [i for i in l]
        return redirect(url_for('skills1'))
    return render_template('rate.html',det=det,mng=mng)


@app.route('/adminprofile',methods=['GET','POST'])
def adminprofile():
    cursor = connection1.cursor()
    cursor.execute("select skill,round( (avg(cast(rating as float))+avg(cast(isnull(mngrat,rating) as float)))/2 ,2) from skills group by skill")
    l1 = cursor.fetchall()  # data from database
    print(l1)
    d1= {'Skill': 'Avg rating in a particular skill'}
    for i in l1:
        d1[str(i[0])] = i[1]
    data1 = d1
    cursor = connection1.cursor()
    cursor.execute("SELECT skill,count(rating) FROM skills group by skill ;")
    l2 = cursor.fetchall()  # data from database
    d2= {'Skill': 'No. of employees in each skill'}
    for i in l2:
        d2[str(i[0])] = i[1]
    print(d2)
    cursor.execute("select skill,round( (avg(cast(rating as float))+avg(cast(isnull(mngrat,rating) as float)))/2 ,2) from skills where empid in(select empid from profile where location='USA') group by skill ")
    l3 = cursor.fetchall()  # data from database
    print(l3)
    d3= {'Skill': 'Avg rating'}
    for i in l3:
        d3[str(i[0])] = i[1]
    data3 = d3
    print(data3)
    cursor.execute("select round( (avg(cast(rating as float))+avg(cast(isnull(mngrat,rating) as float)))/2 ,2) from skills ")
    c = cursor.fetchone()  # data from database
    rating1 = c[0]

    cursor.execute("select  profile.location ,count(distinct skill) from skills inner join profile on profile.empid=skills.empid group by location ;")
    l5 = cursor.fetchall()  # data from database
    d5 = {}
    for i in l5:
        d5[i[0]] = i[1]
    d5= {k: d5[k] for k in sorted(d5, key=d5.get)}
    data5 = {'Location': 'No. of skills'}
    data5.update(d5)

    cursor.execute("select skill,round( (avg(cast(rating as float))+avg(cast(isnull(mngrat,rating) as float)))/2 ,2) from skills where empid in(select empid from profile where location='Bangalore') group by skill  ")
    l6 = cursor.fetchall()  # data from database
    d6= {}
    for i in l6:
        d6[i[0]] = i[1]
    d6 = {k: d6[k] for k in sorted(d6, key=d6.get)}
    data6 = {'Skill': 'Avg rating'}
    data6.update(d6)
    cursor.execute("select skill,round( (avg(cast(rating as float))+avg(cast(isnull(mngrat,rating) as float)))/2 ,2) from skills where empid in(select empid from profile where location='Hyderabad') group by skill  ")
    l7 = cursor.fetchall()  # data from database
    d7 = {}
    for i in l7:
        d7[i[0]] = i[1]
    d7 = {k: d7[k] for k in sorted(d7, key=d7.get)}
    data7 = {'Skill': 'Avg rating'}
    data7.update(d7)
    cursor.execute("select skill,count(distinct empid)  from skills group by skill")
    l9 = cursor.fetchall()  # data from database
    d9 = {}
    for i in l9:
        d9[i[0]] = i[1]
    # d9 = {k: d9[k] for k in sorted(d9, key=d9.get)}
    data9 = {'Skill': 'N0. of employees'}
    data9.update(d9)
    print(data9)
    cursor.execute(
        "select skill,count(distinct skills.empid)  from skills inner join profile on profile.empid=skills.empid where profile.location='USA' group by skill")
    l9 = cursor.fetchall()  # data from database
    d9 = {}
    for i in l9:
        d9[i[0]] = i[1]
    # d9 = {k: d9[k] for k in sorted(d9, key=d9.get)}
    data9 = {'Skill': 'No. of employees'}
    data9.update(d9)
    print(data9)

    cursor.execute(
        "select skill,count(distinct skills.empid)  from skills inner join profile on profile.empid=skills.empid where profile.location='Bangalore' group by skill")
    l10 = cursor.fetchall()  # data from database
    d10 = {}
    for i in l10:
        d10[i[0]] = i[1]
    # d9 = {k: d9[k] for k in sorted(d9, key=d9.get)}
    data10 = {'Skill': 'No. of employees'}
    data10.update(d10)
    print(data10)

    cursor.execute(
        "select skill,count(distinct skills.empid)  from skills inner join profile on profile.empid=skills.empid where profile.location='Hyderabad' group by skill")
    l11 = cursor.fetchall()  # data from database
    d11 = {}
    for i in l11:
        d11[i[0]] = i[1]
    # d9 = {k: d9[k] for k in sorted(d9, key=d9.get)}
    data11 = {'Skill': 'No. of employees'}
    data11.update(d11)
    print(data11)
    return render_template('adminprofile.html', data1=data1, d2=d2, data3=data3, data5=data5, data6=data6, data7=data7, rating1=rating1, data9=data9, data10=data10, data11=data11)




@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))


global drop


@app.route('/adduser',methods=['POST', 'GET'])
def adduser():
    global drop
    cursor = connection1.cursor()
    cursor.execute("select empid from signin where mngid is NULL")
    drop2 = cursor.fetchall()
    drop = [int(i[0]) for i in drop2]

    if request.method == 'POST':

        emp = request.form['empid']
        passd = request.form['password']
        match2 = re.match("^2[0-9]{3}$", emp)
        if emp=='' or passd=='':
            flash('Empid and password are mandatory', 'danger')
            return redirect(url_for('adduser'))
        elif match2==None:
            flash('Employee Id must be 4 digited starting with 2','danger')
            return redirect(url_for('adduser'))
        mngd = request.form['mngid']
        cursor = connection1.cursor()

        cursor.execute("select empid from signin where empid='" + emp + "'")
        l = cursor.fetchall()
        cursor.execute("select empid from old_signin where empid='" + emp + "'")
        m = cursor.fetchall()

        if l == [] and m==[]:
            if mngd != '-':
                insert = ("INSERT INTO signin"
                          "(empid,password,mngid)"
                          "VALUES(?,?,?)")
                hashed_password = bcrypt.generate_password_hash(passd).decode('utf-8')
                values = [emp, hashed_password, mngd]
            else:
                insert = ("INSERT INTO signin"
                          "(empid,password)"
                          "VALUES(?,?)")
                hashed_password = bcrypt.generate_password_hash(passd).decode('utf-8')

                values = [emp, hashed_password]
            cursor.execute(insert, values)
            connection1.commit()
            cursor = connection1.cursor()
            cursor.execute("select empid from signin where mngid is NULL")
            drop2 = cursor.fetchall()
            drop = [int(i[0]) for i in drop2]

            flash("Employee added succesfully", 'success')
        else:
            flash("Employee already exists", 'danger')
            return redirect(url_for('adduser'))
    return render_template('adduser.html',drop=drop)


@app.route('/deleteuser',methods=['POST', 'GET'])
def deleteuser():
    form = DeleteuserForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            result = request.form
            cursor = connection1.cursor()
            values = list(result.values())
            cursor.execute("select empid,mngid from signin where empid='" + values[1] + "'")
            l = cursor.fetchall()
            if l == []:
                flash("Employee doesn't exists",'danger')
            else:
                empid=l[0][0]
                mngid=l[0][1]
                if mngid != None:
                    cursor.execute("delete from signin where empid='" + empid + "'")
                else:
                    cursor.execute("delete from signin where empid='" + empid + "'")
                    cursor.execute("update signin set mngid='not_assigned' where mngid='" + empid + "'")
                    flash("Employee deleted Successfully", 'success')
            connection1.commit()
    return render_template('deleteuser.html',form=form)


@app.route('/updateuser',methods=['POST', 'GET'])
def updateuser():
    global drop
    cursor = connection1.cursor()
    cursor.execute("select empid from signin where mngid is NULL")
    drop2 = cursor.fetchall()
    drop = [int(i[0]) for i in drop2]

    if request.method == 'POST':

        emp = request.form['empid']

        if emp == '':
            flash('Empid is mandatory field','danger')
            return redirect(url_for('updateuser'))

        mngd = request.form['mngid']
        cursor = connection1.cursor()

        cursor.execute("select empid,mngid from signin where empid='" + emp + "'")
        u = cursor.fetchall()
        if u == []:
            flash("Employee doesn't exists",'danger')
        else:
            empid=u[0][0]
            mngid=u[0][1]
            if mngid == None:
                flash('you cannot update','danger')
            else:
                cursor = connection1.cursor()
                cursor.execute("update signin set mngid = '" + mngd + "' where empid='" + emp + "'")
                connection1.commit()
                flash('Updated Succesfully', 'success')
                cursor = connection1.cursor()
                cursor.execute("select empid from signin where mngid is NULL")
                drop2 = cursor.fetchall()
                drop = [int(i[0]) for i in drop2]
    return render_template('updateuser.html',drop=drop)


@app.route('/addskill', methods=['POST', 'GET'])
def addskill():
    form = SkillForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            result = request.form
            cursor = connection1.cursor()
            values = list(result.values())
            cursor.execute("select * from skill_list")
            l = cursor.fetchall()
            lit= [i[0] for i in l]

            if values[1] in lit:
                flash("Already skill exists",'danger')
                return redirect(url_for('addskill'))
            else:
                cursor.execute("insert into skill_list(skill) values('" + values[1] + "')")
                connection1.commit()
                flash('Skill added successfully','success')
    return render_template('addskill.html', form=form)


@app.route('/skillmatrix', methods=['POST', 'GET'])
def skillmatrix():
    cursor = connection1.cursor()
    cursor.execute("select * from skill_list order by skill")
    l=cursor.fetchall()
    skill=[i[0] for  i in l]
    cursor.execute("select * from skill_matrix_view")
    l3=cursor.fetchall()
    print(l3)
    rates=[]
    for row in l3:
        sk=[]
        row=list(row)
        for i in row:
            if i is not None:
                sk.append(str(i))
            else :
                sk.append('-')
        rates.append(sk)
    l3=rates
    return render_template('skillmatrix.html',skill=skill,l3=l3)


if __name__ == '__main__':
    app.run(debug=True)
