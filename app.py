import base64
import re
from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    request,
    session,
    url_for,
)
from dbhelper import *
from sqlite3 import IntegrityError

uploadfolder = "static/images"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = uploadfolder
app.config["SECRET_KEY"] = "!@#$#$%#"


@app.after_request
def add_cache_control(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    # response.headers["Pragma"] = "no-cache"
    # response.headers["Expires"] = "0"
    return response


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Query to check if user exists
        user = get_user(username, password)

        if user:
            session["username"] = username
            return redirect(url_for("student_list"))
        else:
            flash("Invalid username or password!")
            return redirect("/")

    return render_template("login.html", pagetitle="Student Information")


# Student list route (protected route, accessible only after login)
@app.route("/student_list")
def student_list():
    if "username" not in session:
        flash("Please login first!")
        return redirect(url_for("login"))

    students = get_students()
    return render_template(
        "student.html", students=students, pagetitle="Student Information"
    )


# Logout route
@app.route("/logout")
def logout():
    session.clear()  # Clear all session data
    flash("You have been logged out.")
    return redirect(url_for("login"))


# saveinfo route
@app.route("/saveinformation", methods=["POST"])
def saveinformation():
    idno = request.form.get("idno")
    lastname = request.form.get("lastname")
    firstname = request.form.get("firstname")
    course = request.form.get("course")
    level = request.form.get("level")

    # Get the base64 webcam image data and save it
    webcam_data = request.form.get("webcam")
    if webcam_data:
        image_data = re.sub("^data:image/jpeg;base64,", "", webcam_data)
        # imagename = f"{uploadfolder}/{idno}.jpeg"
        imagename = uploadfolder + "/" + idno + ".jpeg"
        with open(imagename, "wb") as fh:
            fh.write(base64.b64decode(image_data))
    else:
        flash("Error: No image file found")
        return redirect("/student_list")

    # Add record to database
    try:
        # Attempt to add the record
        ok = add_record(
            "students",
            idno=idno,
            lastname=lastname,
            firstname=firstname,
            course=course,
            level=level,
            image=imagename,
        )
        message = "Student ADDED" if ok else "Error adding Student"
    except IntegrityError:
        flash("Error: IDNO already exists.")
        return redirect("/student_list")
    flash(message)
    return redirect("/student_list")


# delete student route
@app.route("/deletestudent", methods=["POST"])
def deletestudent():
    idno = request.form.get("idno")

    # Delete the student record from the database
    ok = delete_record("students", idno=idno)
    message = "Student DELETED" if ok else "Error deleting Student"
    flash(message)

    return redirect("/student_list")


# update student
@app.route("/updateinformation", methods=["POST"])
def updateinformation():
    idno = request.form.get("idno")
    lastname = request.form.get("lastname")
    firstname = request.form.get("firstname")
    course = request.form.get("course")
    level = request.form.get("level")

    # Check if the webcam image has been updated
    webcam_data = request.form.get("webcam")
    if webcam_data:
        image_data = re.sub("^data:image/jpeg;base64,", "", webcam_data)
        # imagename = f"{uploadfolder}/{idno}.jpeg"
        imagename = uploadfolder + "/" + idno + ".jpeg"
        with open(imagename, "wb") as fh:
            fh.write(base64.b64decode(image_data))

    # Update student record in the database
    ok = update_record(
        "students",
        idno=idno,
        lastname=lastname,
        firstname=firstname,
        course=course,
        level=level,
        image=imagename,
    )
    message = "Student UPDATED" if ok else "Error updating Student"
    flash(message)
    return redirect("/student_list")


@app.route("/")
def index() -> None:
    return render_template("login.html", pagetitle="Student Information")


if __name__ == "__main__":
    app.run(debug=True)
