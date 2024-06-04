from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config # type: ignore
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, logout_user, login_required 

app = Flask(__name__)

app.config.from_object(Config) 
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from forms import ContactForm, LoginForm, RegistrationForm, ResetPasswordForm # type: ignore
from models import User, Contact # type: ignore

@app.route('/')
def hello_world():
    return render_template("index.html", title="Homepage")

@app.route('/gallery')
def gallery():
    return render_template("gallery.html", title="Photo Gallery")

@app.route('/history')
def history():
    return render_template("history.html", title="History of Ngunnawal") 

@app.route('/grid')
def grid():
    return render_template("grid.html", title="Bootstrap Grid") 

@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for("homepage"))
    return render_template("contact.html", title="Contact Us", form=form, user=current_user)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email_address=form.email_address.data, name=form.name.data, user_level=1, active=True) # defaults to regular user
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("homepage"))
    return render_template("registration.html", title="User Registration", form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        print(user)
        if user is not None and user.check_password(form.password.data):
            # User has been authenticated
            login_user(user)
            print("DEBUG: Login Successful")
            return redirect(url_for("homepage"))
        else:
            print("DEBUG: Login Failed")
            # Username or password incorrect
            return redirect(url_for("login"))
    return render_template("login.html", title="Login", form=form)

@app.route('/passwordreset', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=current_user.email_address).first()
        user.set_password(form.new_password.data)
        db.session.commit()
        flash("Your password has been changed.")
        return redirect(url_for('homepage'))
    return render_template("passwordreset.html", title='Reset Password', form=form, user=current_user)


@app.route('/contact_messages')
@login_required
def view_contact_messages(): contact_messages = Contact.query.all()
