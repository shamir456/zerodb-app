# coding: utf-8
"""
ZeroDB application example
"""
from flask import (Flask, render_template, redirect,session,
                   url_for, request, jsonify, abort, make_response, flash)
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, DateField, SelectField,DateTimeField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import models
from database import ZeroDBStorage
import json
from flask_wtf.csrf import CSRFProtect
# from wtforms.fields.html5 import DateTimeLocalField
import datetime

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
    password = PasswordField("password",validators=[DataRequired()])
    submit   = SubmitField('Submit')

class DoctorRegistryEditor(Form):
    name     = StringField("username", validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])
    specialization = StringField("specialization", validators=[DataRequired()])
    email    = StringField("Email",validators=[DataRequired()])
    submit   =  SubmitField('Submit')

class ReceptionistRegistryEditor(Form):
    name     = StringField("username", validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])
    email    = StringField("Email",validators=[DataRequired()])
    submit   =  SubmitField('Submit')

class AppointmentTemplate(Form):
    name= StringField("patient_name", validators=[DataRequired()])
    # date= DateField("arrival_Date",format='%Y-%m-%d', validators=[DataRequired()])
    # date = DateTimeLocalField('Which date is your favorite?', format='%Y-%m-%d %H:%M:%S')
    date_time = DateTimeField(
        "date_time", format="%Y-%m-%dT%H:%M:%S",
        default=datetime.datetime.now(), ## Now it will call it everytime.
        validators=[DataRequired()]
    )

    doctor_name = SelectField('Name',
                        choices=[])
    reception_name=StringField("reception_name",)
    age= StringField("age", validators=[DataRequired()])
    bloodgroup= SelectField(
        'bloodgroup',
        choices=[('A', 'A'), ('AB', 'AB'), ('O+', 'O+'),('O-', 'O-')]
    )
    submit =  SubmitField('Submit')



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


@app.route("/viewpatients", methods=["GET", "POST"])
def view_patients():
    """
    Index Page
    """
    try:
        zero = ZeroDBStorage()
        patients = zero._get_appointments()
        print(patients)
        patient_date=patients[0].date_time
        print(patient_date)
        date = datetime.datetime.strptime(patient_date, "%Y-%m-%d %H:%M:%S")
        print(date.year)
        # date_app=date.year+'-'+date.month+'-'+date.day
        # print(date_app)
        # time_app=date.hour+':'+date.minute
        # print(date_app)

        
        return render_template("current_patients.html", myPatients=patients)
    except Exception as e:
        # flash('Cannot get posts in database: ' + str(e))
        return render_template("current_patients.html")

@app.route("/admin_dashboard/viewdoctors")
def view_doctors():
    """
    Index Page
    """
    try:
        zero = ZeroDBStorage()
        doctors=zero._get_doctors()
        print(doctors)
        # if zero._delete('k164030@u.edu.pk'):
        #     print('Deleted')
        # else:
        #     print('FAiled')

        # patients = zero._get()
        
        return render_template("current_doctors.html", myDoctors=doctors)
    except Exception as e:
        flash('Cannot get posts in database: ' + str(e))
        return render_template("current_doctors.html", alert=error)

@app.route("/admin_dashboard/viewreceptions")
def view_receptions():
    """
    Index Page
    """
    try:
        zero = ZeroDBStorage()
        receptionist = zero._get_receptionist()
        print(receptionist)
        
        return render_template("current_reception.html", myReception=receptionist)
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
        cred = {
            'email': username,
            'password': password
        }


        zero = ZeroDBStorage()
        verified,receptionist=zero._authenticate_receptionist(cred=cred)

        if verified:
            session['receptionist_id']=str(receptionist.recep_id)
            session['reception_name']=str(receptionist.name)
            print(session['receptionist_id'])
            return redirect("/reception_dashboard")
        else:
            flash('Cannot Login Receptionist')
        # return render_template('reception_dashboard.html', form=form)
    return render_template('reception_login.html', form=form)


# @app.route("/del/id=<string:post_id>", methods=['GET'])
# def del_post(post_id):
#     try:
#         zero = ZeroDBStorage()
#         result = zero._delete(pid=post_id)
#         if result:
#             return redirect('/')
#     except Exception as e:
#         flash('Cannot delete this post: ' + str(e))
#         return redirect(url_for("get_post", post_id=post_id))

@app.route("/admin_dashboard/<string:doctor_id>/", methods=['GET'])
def del_doctor(doctor_id):
    try:
        zero = ZeroDBStorage()
        print(doctor_id)
        result = zero._delete_doctor(doctor_id=doctor_id)
        if result:
            return redirect(url_for("reception_dashboard"))
    except Exception as e:
        print('kk')
        # flash('Cannot delete this post: ' + str(e))
        return redirect(url_for("reception_dashboard"))

@app.route("/receptionist/del/id=<string:recep_id>", methods=['GET'])
def del_receptionist(post_id):
    try:
        zero = ZeroDBStorage()
        result = zero._delete(pid=post_id)
        if result:
            return redirect('/')
    except Exception as e:
        flash('Cannot delete this post: ' + str(e))
        return redirect(url_for("get_post", post_id=post_id))

@app.route("/reception_dashboard/Appointmentform", methods=["GET", "POST"])
def add_appointment():
    print("dsadasdas")
    zero = ZeroDBStorage()
    doctors=zero._get_doctors()
    print(doctors)

    form = AppointmentTemplate(request.form)
    form.doctor_name.choices = [(str(i.doctor_id), i.name) for i in doctors]

    print(form.name.data)
    if form.validate_on_submit():
        print(form.name.data)
        p_name = form.name.data
        date_time = form.date_time.data
        doc_name= form.doctor_name.data
        receptionist_name= form.reception_name.data
        age= form.age.data
        bloodgroup=form.bloodgroup.data
        print('patient name',p_name)
        print('date of appointment',date_time)
        print('doctor name',doc_name)
        print('receptionist_name',receptionist_name)
        print('Age',age)
        print('bloodgroup',bloodgroup)
        appointment = {
                'receptionist_id': session['receptionist_id'],
                'age': age,
                'doctor_id':doc_name,
                'bloodgroup':bloodgroup,
                'datetime':str(date_time),
                'patient_name':p_name
            }
        print(appointment)
        zero = ZeroDBStorage()
        if zero._create_appointment(appointment=appointment):
            # return redirect('/')
            return render_template('success.html')

        else:
            flash('Cannot Add appointment')
    return render_template('appointment_form.html', form=form)


@app.route("/admin_dashboard/doctor_registry", methods=["GET", "POST"])
def add_doctor():
    print("adding doctor")
    form = DoctorRegistryEditor()
    print(form.name.data)
    if form.validate_on_submit():
        print(form.name.data)
        name = form.name.data
        specialization = form.specialization.data
        email= form.email.data
        password= form.password.data
        print(name)
        print(email)
        print(password)
        print(specialization)
        doctor = {
                'name': name,
                'specialization': specialization,
                'email':email,
                'password':password
            }
        zero = ZeroDBStorage()
        if zero._create_doctor(doctor=doctor):
            return render_template('doctor_success.html', form=form)
        else:
            print('Cannot Add')
    return render_template('doctor_registry.html', form=form)
    
@app.route("/admin_dashboard/receptionist_registry", methods=["GET", "POST"])
def add_receptionist():
    print("adding receptionist")
    form = ReceptionistRegistryEditor()
    print(form.name.data)
    if form.validate_on_submit():
        print(form.name.data)
        name = form.name.data
        email= form.email.data
        password= form.password.data
        print(name)
        print(email)
        print(password)
        receptionist = {
                'name': name,
                'email': email,
                'password':password
            }
        print(receptionist)
        zero = ZeroDBStorage()
        if zero._create_receptionist(reception=receptionist):
            return redirect("/d_add_succesfully")

            # return redirect('/')
        else:
            print('Not Done')
    return render_template('receptionist_registry.html', form=form)
      

@app.route("/login/doctor_login/", methods=["GET", "POST"])
def doctor_login():
    form = LoginEditor()
    zero = ZeroDBStorage()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username,password)
        cred = {
            'email': username,
            'password': password
        }
        # zero = ZeroDBStorage()
        if zero._authenticate_doctor(cred=cred):
            return redirect("/viewpatients")
        else:
            flash('Cannot Login doctor')
        #     # return redirect('/')
        # else:
        # flash(username+'  '+password)
        # return render_template("current_patients.html", myPatients=Temp_patients)
    return render_template('doctor_login.html', form=form)
        
@app.route("/login/admin_login/", methods=["GET", "POST"])
def admin_login():
    form = LoginEditor()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username,password)
        cred = {
            'email': username,
            'password': password
        }
        zero = ZeroDBStorage()
        if zero._authenticate_admin(cred=cred):
            return redirect('/admin_dashboard')
            # return redirect('/')
        else:
            flash('Cannot Login Admin')
        
    return render_template('admin_login.html', form=form)



@app.route("/login", methods=["GET", "POST"])
def login_student():
    try:
        sp={"email": "k164030@nu.edu.pk",
            "password": "Hello111",
            "specialization":"EPD",
            "name":"mmmm"}
        zero=ZeroDBStorage()
        print( zero._get_doctors())
    except Exception as e:

        flash('Cannot ')
        # return redirect(url_for("get_post", post_id=post_id))


    return render_template('login.html')

@app.route("/reception_dashboard", methods=["GET", "POST"])
def reception_dashboard():
        return render_template('reception_dashboard.html')

@app.route("/admin_dashboard", methods=["GET", "POST"])
def admin_dashboard():
        return render_template('admin_dashboard.html')

@app.route("/addsuccesfully", methods=["GET", "POST"])
def success():
        return render_template('success.html')

@app.route("/d_add_succesfully", methods=["GET", "POST"])
def dsuccess():
        return render_template('doctor_success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
