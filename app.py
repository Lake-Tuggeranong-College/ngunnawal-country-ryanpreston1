from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html", title="Homepage")


@app.route('/contact')
def contact():
    return render_template("contact.html", title="Contact Us") 

@app.route('/gallery')
def gallery():
    return render_template("gallery.html", title="Photo Gallery")


@app.route('/history')
def history():
    return render_template("history.html", title="History of Ngunnawal") 

@app.route('/grid')
def grid():
    return render_template("grid.html", title="Bootstrap Grid") 

from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config # type: ignore
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, logout_user, login_required 

app.config.from_object(Config) 
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from forms import ContactForm, LoginForm, RegistrationForm, ResetPasswordForm, UserProfileForm # type: ignore
from models import User, Contact # type: ignore

@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for("homepage"))
    return render_template("contact.html", title="Contact Us", form=form, user=current_user)