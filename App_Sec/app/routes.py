#!/user/bin/python3.6
import os
from app import app, db
from app.models import User, Image
from app.forms import LoginForm, RegistrationForm
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, \
session, escape
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import logging
import PIL
from PIL import Image as im

UPLOAD_FOLDER = "/home/danny/Documents/Programs/App_Sec/uploads"
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png", "bmp", "gif"])

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_PATH"] = 2048

app.secret_key = os.urandom(32) #Random 32 byte session key

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part?")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file!")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            file = square(filename, int(list(request.form.items())[0][1]))
            filename = "square_" + filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            if current_user.is_authenticated:
                image = Image(url=filename, author=current_user)
                try:
                    db.session.add(image)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                    flash("Saved!")
                    app.logger.info("USER: %s uploaded %s", current_user.username, file.filename)
                except Exception as e:
                    return redirect(url_for("uploaded_file", filename=filename))
        
                return redirect(url_for("uploaded_file", filename=filename))
                #return redirect(url_for("index")) #Broken so I'm not using the gallery approach for now
            else:
                #return redirect(url_for("uploaded_file", filename=filename))
                return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
        else:
            flash("Something went wrong!")
            if current_user.is_authenticated:
                app.logger.warning("USER: %s unsuccessfully attempted to upload %s", current_user.username, file.filename)

            return render_template("upload.html") 

    return render_template("upload.html") 
        
def square(image_name, width):

    img = im.open(image_name)
    if current_user.is_authenticated:
        app.logger.info("USER: %s resized %s", current_user.username, image_name)
    else:
        app.logger.info("USER: Anonymous resized %s", image_name)
    return img.resize((width, width), im.ANTIALIAS)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    if current_user.is_authenticated: 
        for image in current_user.images.all():
            if filename == image.url:
                #if os.path.join(app.config["UPLOAD_FOLDER"], filename) in current_user.images.all():
                app.logger.info("USER: %s successfully uploaded %s", current_user.username, filename)
                return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    else:
        return render_template("upload.html")
    return render_template("upload.html")
    #else:
    #    return redirect(url_for("index"))

@app.route("/gallery")
def gallery():
    user = current_user
    if current_user.is_authenticated:
        return render_template("gallery.html", user=user)
    else:
        return redirect(url_for("register"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            app.logger.warning("USER: %s failed login", user)
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        app.logger.info("USER: %s logged in successfully", current_user.username)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route("/logout")
def logout():
    username = current_user.username
    logout_user()
    app.logger.info("USER: %s logged out successfully", username)
    return redirect(url_for("index"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        app.logger.info("USER: %s registered successfully", user)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
