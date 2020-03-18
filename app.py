from flask import Flask, render_template, url_for, redirect, flash, request ,session,jsonify
import os
import secrets
import pypyodbc
from forms import LoginForm,ProfileForm,AdminLoginForm,ForgotForm,ResetForm,ResetpassForm,SearchForm,SkillsForm,AdminRegistrationForm
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
            # pass1 = form.password.data
            cursor.execute(select, [name1])
            results = cursor.fetchone()
            mng = results[2]

            if results !=None:
                password = results[1]
                if name1 in results and bcrypt.check_password_hash(password, form.password.data):
                    session['user'] = True
                    select1 = "select * from profile where empid ='"+name1+"'"
                    cursor.execute(select1)
                    results1 = cursor.fetchone()
                    if results1!=None:
                        if mng != None:
                            return redirect(url_for('skills'))
                        else:
                            return redirect(url_for('skills1'))
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
            if mng != None:
                return redirect(url_for('skills'))
            else:
                return redirect(url_for('skills1'))
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



@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    cursor = connection1.cursor()
    global a

    cursor.execute("select skill,rating from skills where empid ='" + a + "' ")
    l1 = cursor.fetchall()  # data from database
    d1= {}
    for i in l1:
        d1[i[0]] = i[1]
    # d1 = {k: d1[k] for k in sorted(d1, key=d1.get)}
    data1 = {'Skill': 'Rating'}
    print(data1)
    data1.update(d1)

    cursor.execute("select round((sum(rating))/(count(*)),1) from skills where empid ='" + a + "'  group by empid")
    bb = cursor.fetchone()  # data from database
    rating = bb[0]


    cursor = connection1.cursor()
    cursor.execute("with cte as(select max(rating) as m,skill from skills group by skill) select s.skill,s.rating,c.m from skills s inner join cte c on s.skill=c.skill where empid='" + a + "' ")
    l3 = cursor.fetchall()  # data from database
    # d = {}
    cursor.execute("select distinct count(skill) from skills where empid='" + a + "' ")
    j3= cursor.fetchall()
    k3 = j3[0][0]
    n=[*range(k3)]
    t3=[]
    for i in l3:
        t3.append(list(i[0:]))
    m3= sorted(t3, key=lambda x: x[1])

    data3=m3
    print(m3)

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
    print(d1)
    sk = [[i,j[0]] for i,j in d1.items()]
    print(sk)

    return render_template('dashboard.html',mng=mng,rating=rating, data1=data1,data3=data3,n=n,sk=sk)


@app.route('/dashboard1')
def dashboard1():
    cursor = connection1.cursor()
    cursor.execute("select round((sum(p.rating)+sum(p.mngrat))/(2*count(*)),1) from skills p full outer join signin s on s.empid=p.empid where s.mngid='"+a+"'")
    h = cursor.fetchone()  # data from database
    rat = h[0]
    print(rat)

    cursor = connection1.cursor()
    cursor.execute("select p.skill, round((sum(p.rating) + sum(p.mngrat)) / (2 * count(*)), 1) from skills p full outer join signin s on s.empid = p.empid  where s.mngid = '"+a+"' group by  p.skill" )
    l5 = cursor.fetchall()  # data from database
    d5 = {}
    for i in l5:
        d5[i[0]] = i[1]
    # d5 = {k: d5[k] for k in sorted(d5, key=d5.get)}
    data5 = {'Skill': 'Rating'}
    data5.update(d5)
    print(data5)
    return render_template('dashboard1.html',mng=mng,rat=rat,data5=data5)



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


global data2;


@app.route('/skills',methods=['POST','GET'])
def skills():
    cursor = connection1.cursor()
    cursor.execute("select skill,rating from skills where empid='" + a + "'")
    global data2
    data2 = cursor.fetchall()
    form = SkillsForm()
    return render_template('skills.html', value=data2, form=form, mng=mng)

@app.route('/add',methods=['POST','GET'])
def add():
    cursor = connection1.cursor()
    cursor.execute("select skill,rating from skills where empid='" + a + "'")
    global data2
    data2 = cursor.fetchall()
    cursor.execute("select skill from skills where empid='" + a + "'")
    db = cursor.fetchall()
    existing = [i[0] for i in db]
    print(existing)
    form = SkillsForm()
    if form.validate_on_submit():
        if request.method == "POST":
            result = request.form
            cursor = connection1.cursor()
            values = list(result.values())
            print(values)
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
            else:
                flash('This skill is already added', 'danger')
    return render_template('skills.html', form=form, value=data2, mng=mng)


@app.route('/edit',methods=['POST','GET'])
def edit():
    if request.method == "POST":
        global data2
        n=len(data2)
        rates=[]
        for i in range(1,n+1):
            rates.append(request.form['rate'+str(i)])
        cursor = connection1.cursor()
        for i in range(0,n):
            update = "UPDATE skills set rating=? where empid='" + a + "' and skill = '" + data2[i][0]+ "'"
            values=[rates[i]]
            cursor.execute(update,values)
        connection1.commit()
        return redirect(url_for('add'))
    return render_template('edit.html',value=data2,mng=mng)



@app.route('/delete', methods=['POST','GET'])
def delete():
    form = SkillsForm()
    global data2;
    if request.method == "POST":
        cursor = connection1.cursor()
        x1 = request.form['dlt']
        print(x1)
        sk = data2[int(x1) - 1][0]
        update = "DELETE from skills where empid='" + a + "' and skill = '" + sk + "'"
        cursor.execute(update)
        connection1.commit()
        cursor.execute("select skill,rating from skills where empid='" + a + "'")
        data2 = cursor.fetchall()
    return render_template('skills.html', value=data2,form=form, mng=mng)


@app.route('/skills1')
def skills1():
    cursor = connection1.cursor()
    cursor.execute("with cte as(select empid from signin where mngid='"+ a +"')"
    "select s.empid,p.fname+p.lname from cte s inner join profile p on p.empid=s.empid")
    value = cursor.fetchall()
    return render_template('skills1.html',value=value,mng=mng)


@app.route('/search',methods=['GET','POST'])
def search():
    form=SearchForm()
    if form.validate_on_submit():
        if request.method=='POST':
            values=list(request.form.values())
            cursor=connection1.cursor()
            select=("with cte as (select p.*,s.rating,s.skill from profile p  inner join skills s on s.empid=p.empid)"
            "select * from cte where skill like ? and rating like ? and location like ? and practice like ? and experience like ? and currentpro like ?")
            values=[values[1],values[4],values[6],values[5],values[3],values[2]]
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
            if bcrypt.check_password_hash(results2[0], values[1]):
            # if values[1]==results2[0]:
                if values[2] == values[3]:
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
    print(t)
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
    return render_template('rate.html',det=det,mng=mng)


@app.route('/adminprofile',methods=['GET','POST'])
def adminprofile():
    cursor = connection1.cursor()
    cursor.execute("SELECT skill,(sum(rating)+sum(mngrat))/(2*count(*)) FROM skills group by skill ;")
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
    data2 = d2

    cursor.execute("with cte as(SELECT p.fname, p.location, s.skill, s.rating FROM skills s FULL OUTER JOIN profile p ON p.empid=s.empid where p.location='USA') select skill, count(skill) from cte group by skill ")
    l3 = cursor.fetchall()  # data from database
    print(l3)
    d3= {'Skill': 'Avg rating'}
    for i in l3:
        d3[str(i[0])] = i[1]
    data3 = d3
    print(data3)

    cursor.execute("select round((sum(rating)+sum(mngrat))/(2*count(*)),1) from skills ")
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


    cursor.execute("with cte as(SELECT p.fname, p.location, s.skill, s.rating FROM skills s FULL OUTER JOIN profile p ON p.empid=s.empid where p.location='Bangalore') select skill, count(skill) from cte group by skill ")
    l6 = cursor.fetchall()  # data from database
    d6= {}
    for i in l6:
        d6[i[0]] = i[1]
    d6 = {k: d6[k] for k in sorted(d6, key=d6.get)}
    data6 = {'Skill': 'Avg rating'}
    data6.update(d6)

    cursor.execute("with cte as(SELECT p.fname, p.location, s.skill, s.rating FROM skills s FULL OUTER JOIN profile p ON p.empid=s.empid where p.location='Hyderabad') select skill, count(skill) from cte group by skill ")
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

    return render_template('adminprofile.html', data1=data1, data2=data2, data3=data3, data5=data5, data6=data6, data7=data7, rating1=rating1, data9=data9, data10=data10, data11=data11)




@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))




@app.route('/adduser',methods=['POST','GET'])
def adduser():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            result = request.form
            cursor = connection1.cursor()
            values = list(result.values())
            if values[3]!='-':
                insert = ("INSERT INTO signin"
                          "(empid,password,mngid)"
                          "VALUES(?,?,?)")
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                values = [values[1], hashed_password, values[3]]
            else:
                insert = ("INSERT INTO signin"
                          "(empid,password)"
                          "VALUES(?,?)")
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

                values = [values[1], hashed_password]
            cursor.execute(insert, values)
            connection1.commit()
    return render_template('adduser.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
