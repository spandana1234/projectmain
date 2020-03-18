from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired,Email,Length,EqualTo


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
    skills=[('%','Select'),('Java','Java'),('Python','Python'),('C++','C++'),('Java Script','Java Script'),
            ('SQL','SQL'),('c#','c#'),('Scala','Scala')]
    skills1=SelectField(choices=skills)
    Exp=[('%','Select'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]
    exp1=SelectField(choices=Exp)
    rating= [('%','Select'),('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    rating1 = SelectField(choices=rating)
    practices=[('%','Select'),('Data Engineering','Data Engineering'),('Web developer','Web developer'),
               ('Frontend Developer','Frontend Developer'),('Oracle','Oracle'),('Anaplan','Anaplan')]
    practices1 = SelectField(choices=practices)
    loc=[('%','Select'),('Bangalore','Bangalore'),('Hyderabad','Hyderabad'),('USA','USA')]
    loc1 = SelectField(choices=loc)
    proj=[('%','Select'),('Yes','Yes'),('No','No')]
    pro1=SelectField(choices=proj)
    search=SubmitField('Search')


class SkillsForm(FlaskForm):
    skills=[(None,None),('Java','Java'),('Python','Python'),('C++','C++'),('Java Script','Java Script'),
            ('SQL','SQL'),('c#','c#'),('Scala','Scala')]
    select1 = SelectField(choices=skills)
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

class AdminRegistrationForm(FlaskForm):
    empid = StringField( validators=[DataRequired()])
    password = PasswordField( validators=[DataRequired()])
    manager = StringField( validators=[DataRequired()])
    submit = SubmitField('Add User')