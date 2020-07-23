from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired,Email,Length,EqualTo
import pypyodbc

connection1 = pypyodbc.connect(
    "Driver={SQL Server};"
    "Server=LAPTOP-PB290PQU;"
    "Database=project;"
    "Trusted_Connection=yes;"
)


class LoginForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Submit')


class AdminLoginForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Submit')


class ProfileForm(FlaskForm):
    fname = StringField(validators=[DataRequired()])
    lname = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(),Email()])
    exp = StringField(validators=[DataRequired()])
    practices = [('DataEngineering', 'Data Engineering'),
                 ('Webdeveloper', 'Web developer'),
                 ('FrontendDeveloper', 'Frontend Developer'),
                 ('Oracle', 'Oracle'),
                 ('Anaplan', 'Anaplan')]
    select1 = SelectField(choices=practices)
    date = DateField(format='%d/%m/%Y', validators=[DataRequired()])
    projects = [('Yes', 'Yes'),
                ('No', 'No')]
    select2 = SelectField(choices=projects)
    locations = [('USA', 'USA'),
                 ('Hyderabad', 'Hyderabad'),
                 ('Bangalore', 'Bangalore')]
    select3 = SelectField(choices=locations)
    gender = [('Male', 'Male'),
              ('Female', 'Female')]
    select4 = SelectField(choices=gender)
    practices1 = [('Who is your favourite singer/band?', 'Who is your favourite singer/band?'),
                 ('Which state were you born in?', 'Which state were you born in?'),
                 ('What is your favourite car?', 'What is your favourite car?'),
                 ('Which year did you graduated?', 'Which year did you graduated?'),
                 ('What is the name of your pet?', 'What is the name of your pet?')]
    select5 = SelectField(choices=practices1)
    ans = StringField(validators=[DataRequired()])
    submit = SubmitField()


class ForgotForm(FlaskForm):
    empid = StringField(validators=[DataRequired()])
    practices = [('Who is your favourite singer/band?', 'Who is your favourite singer/band?'),
                 ('Which state were you born in?', 'Which state were you born in?'),
                 ('What is your favourite car?', 'What is your favourite car?'),
                 ('Which year did you graduated?', 'Which year did you graduated?'),
                 ('What is the name of your pet?', 'What is the name of your pet?')]
    select1 = SelectField(choices=practices)
    ans = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')


class ResetForm(FlaskForm):
    pwd = PasswordField(validators=[DataRequired()])
    cpwd = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Submit')


class ResetpassForm(FlaskForm):
    old = PasswordField(validators=[DataRequired()])
    new =PasswordField(validators=[DataRequired()])
    cnew = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    s1 = ("SELECT skill, skill "
               "FROM skill_list ")
    cursor = connection1.cursor()
    cursor.execute(s1)
    name = cursor.fetchall()
    result1 = [('%', 'Select')]
    result1.extend(name)

    skills1=SelectField(choices=result1)
    fill = [('current', 'Current Employees'), ('old', 'Old Employees'),('both','Both')]
    fil = SelectField(choices=fill)
    Exp=[('%','Select'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]
    exp1=SelectField(choices=Exp)
    rating= [('0','Select'),('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    rating1 = SelectField(choices=rating)
    practices=[('%','Select'),('DataEngineering','Data Engineering'),('Webdeveloper','Web developer'),
               ('FrontendDeveloper','Frontend Developer'),('Oracle','Oracle'),('Anaplan','Anaplan')]
    practices1 = SelectField(choices=practices)
    loc=[('%','Select'),('Bangalore','Bangalore'),('Hyderabad','Hyderabad'),('USA','USA')]
    loc1 = SelectField(choices=loc)
    proj = [('%','Select'),('Yes','Yes'),('No','No')]
    pro1=SelectField(choices=proj)
    search=SubmitField('Search')


class SkillsForm(FlaskForm):
    select1 = ("SELECT skill, skill "
               "FROM skill_list ")
    cursor = connection1.cursor()
    cursor.execute(select1)
    name = cursor.fetchall()
    result1 = [('None', 'None')]
    result1.extend(name)

    select1 = SelectField(choices=result1)
    rating=[(None,None),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]
    select2 = SelectField(choices=rating)
    submit = SubmitField('Add')


class ProjectForm(FlaskForm):
    projects=StringField(validators=[DataRequired()])
    clients = [(None,None),('Driscolls', 'Driscolls'),
               ('Atlassian', 'Atlassian'),
               ('VMWare', 'VMWare'),
               ('Groupon', 'Groupon'),
               ('Cisco', 'Cisco')]
    clients1 = SelectField(choices=clients)
    manager=[(None,None),('a', 'a'),
               ('b', 'b'),
               ('c', 'c'),
               ('d', 'd'),
               ('e', 'e')]
    manager1=SelectField(choices=manager)
    search = SubmitField('Add')


class DeleteuserForm(FlaskForm):
    empid = StringField(validators=[DataRequired()])
    submit = SubmitField('Delete')


class SkillForm(FlaskForm):
    skill = StringField(validators=[DataRequired()])
    submit = SubmitField('Add')