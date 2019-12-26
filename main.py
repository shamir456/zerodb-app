# coding: utf-8
"""
ZeroDB application example
"""
from flask import (Flask, render_template, redirect,
                   url_for, request, jsonify, abort, make_response, flash)
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import models
from database import ZeroDBStorage
import json
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
Bootstrap(app)
csrf = CSRFProtect(app)
app.config["SECRET_KEY"] = "Hello"

Temp_patients = [
{
  "name":"Fahad",
  "Date":"16-1-19",
  "Time":"7 pm",
  "Age":"20",
  "BldGrp":"A+",
},
{
  "name":"Shameer",
  "Date":"16-1-20",
  "Time":"2 pm",
  "Age":"10",
  "BldGrp":"B+",
},
{
  "name":"Mujtaba Bawani",
  "Date":"13-1-19",
  "Time":"6 pm",
  "Age":"50",
  "BldGrp":"B+",
},
]
Temp_doctors = [
{
  "name":"Ammar Rizwan",
  "email":"test@gmail.com",
  "specialization":"MBBS"
},
{
  "name":"Moazzam Maqsood",
  "email":"test@gmail.com",
  "specialization":"MBBS"
},
{
  "name":"Faizan Saleem",
  "email":"test@gmail.com",
  "specialization":"MBBS"
},
]

Temp_receptionist = [
{
  "name":"Faizan",
  "email":"test@gmail.com",
},
{
  "name":"Abdul Hameed",
  "email":"test@gmail.com",
},
{
  "name":"Tahir Hemani",
  "email":"test@gmail.com",
},
]
class PageDownEditor(Form):
    title = StringField("title", validators=[DataRequired()])
    text = TextAreaField("text", validators=[DataRequired()])
    text2=StringField("text2",validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginEditor(Form):
    username = StringField("username", validators=[DataRequired()])
    password= PasswordField("password",validators=[DataRequired()])
    submit =  SubmitField('Submit')

class AppointmentTemplate(Form):
    name= StringField("patient_name", validators=[DataRequired()])
    date= DateField("arrival_Date", validators=[DataRequired()])
    doctor_name = SelectField('Name', [DataRequired()],
                        choices=[('Farmer', 'farmer'),
                                 ('Corrupt Politician', 'politician'),
                                 ('No-nonsense City Cop', 'cop'),
                                 ('Professional Rocket League Player', 'rocket'),
                                 ('Lonely Guy At A Diner', 'lonely'),
                                 ('Pokemon Trainer', 'pokemon')])
    reception_name=StringField("reception_name", validators =[DataRequired])
    Age= StringField("age", validators=[DataRequired()])
    bloodgroup= StringField("bloodgroup", validators=[DataRequired()])



@app.errorhandler(404)
def not_found(error):
    """
    404 Error
    """
    return make_response(jsonify({"error": "Not Found"}))


@app.errorhandler(400)
def error_in_data(error):
    """
    400 Error
    """
    return make_response(jsonify({"error": "Your data not true"}))


@app.route("/viewpatients")
def view_patients():
    """
    Index Page
    """
    try:
        zero = ZeroDBStorage()
        # patients = zero._get()
        
        return render_template("current_patients.html", myPatients=Temp_patients)
    except Exception as e:
        flash('Cannot get posts in database: ' + str(e))
        return render_template("current_patients.html", alert=error)

@app.route("/admin/viewdoctors")
def view_doctors():
    """
    Index Page
    """
    try:
        zero = ZeroDBStorage()
        # patients = zero._get()
        
        return render_template("current_doctors.html", myDoctors=Temp_doctors)
    except Exception as e:
        flash('Cannot get posts in database: ' + str(e))
        return render_template("current_doctors.html", alert=error)

@app.route("/admin/viewreceptions")
def view_receptions():
    """
    Index Page
    """
    try:
        zero = ZeroDBStorage()
        # patients = zero._get()
        
        return render_template("current_reception.html", myReception=Temp_receptionist)
    except Exception as e:
        flash('Cannot get posts in database: ' + str(e))
        return render_template("current_reception.html", alert=error)


@app.route("/")
def index():
    """
    Index Page
    """
    try:
        zero = ZeroDBStorage()
        posts = zero._get()
        return render_template("index.html", posts=posts)
    except Exception as e:
        flash('Cannot get posts in database: ' + str(e))
        return render_template("index.html", alert=error)


@app.route("/add", methods=["GET", "POST"])
def add_post():
    """
    Add new post to database
    """
    form = PageDownEditor()
    if form.validate_on_submit():
        title = form.title.data
        content = form.text.data
        name=form.text2.data
        print(name,content,title)
        post = {
            'title': title,
            'content': content
        }
        zero = ZeroDBStorage()
        if zero._create(post=post):
            return redirect('/')
        else:
            flash('Cannot add post')
            return render_template('editor.html', form=form)
    return render_template('editor.html', form=form)


@app.route("/post/id=<string:post_id>", methods=['GET', 'POST'])
def get_post(post_id):
    try:
        zero = ZeroDBStorage()
        post = zero._get(pid=post_id)
        return render_template("post.html", post=post[0])
    except Exception as e:
        flash('Cannot get the post with id: '+str(post_id))
        return redirect("/")


@app.route("/del/id=<string:post_id>", methods=['GET'])
def del_post(post_id):
    try:
        zero = ZeroDBStorage()
        result = zero._delete(post_id=post_id)
        if result:
            return redirect('/')
    except Exception as e:
        flash('Cannot delete this post: ' + str(e))
        return redirect(url_for("get_post", post_id=post_id))

@app.route("/login/reception_login/", methods=["GET", "POST"])
def reception():
    form = LoginEditor()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username,password)
        # post = {
        #     'title': title,
        #     'content': content
        # }
        # zero = ZeroDBStorage()
        # if zero._create(post=post):
        #     # return redirect('/')
        # else:
        flash(username+'  '+password)
        return render_template('reception_dashboard.html', form=form)
    return render_template('reception_login.html', form=form)
    

@app.route("/login/doctor_login/", methods=["GET", "POST"])
def doctor_login():
    form = LoginEditor()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username,password)
        # post = {
        #     'title': title,
        #     'content': content
        # }
        # zero = ZeroDBStorage()
        # if zero._create(post=post):
        #     # return redirect('/')
        # else:
        flash(username+'  '+password)
        return render_template("current_patients.html", myPatients=Temp_patients, form=form)
    return render_template('doctor_login.html', form=form)
        
@app.route("/login/admin_login/", methods=["GET", "POST"])
def admin_login():
    form = LoginEditor()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username,password)
        # post = {
        #     'title': title,
        #     'content': content
        # }
        # zero = ZeroDBStorage()
        # if zero._create(post=post):
        #     # return redirect('/')
        # else:
        flash(username+'  '+password)
        return render_template('admin_login.html', form=form)
    return render_template('admin_login.html', form=form)



@app.route("/login", methods=["GET", "POST"])
def login_student():
    try:
        zero=ZeroDBStorage()
        print( zero._get_doctors())
    except Exception as e:

        flash('Cannot ')
        # return redirect(url_for("get_post", post_id=post_id))


    return render_template('login.html')

@app.route("/reception_dashboard", methods=["GET", "POST"])
def reception_dashboard():
        return render_template('reception_dashboard.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
