from flask import Flask , render_template, url_for, redirect, request
from flask import current_app as app
from .models import *

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username=request.form.get("username")
        pd= request.form.get("pd")
        this_user=User.query.filter_by(username=username).first()
        if this_user:
            if this_user.password == pd:
                if this_user.role == "admin":
                    return redirect("/admin_dashboard")
                elif this_user.role == "student":
                    student_dt = this_user.student_profile

                    if student_dt.is_blacklisted == True:
                        return "<h1>you are blacklisted</h1>"
                    else:
                        return redirect (f"/home/{this_user.id}")
                elif this_user.role == "company":
                    comp_data =this_user.company_profile
                    if comp_data.is_approved == True and comp_data.is_blacklisted== False:
                        return redirect(f"/home/{this_user.id}")
                    elif comp_data.is_blacklisted == True:
                         return "<h1>Your company is blacklisted.</h1>"
                    else:
                        return    "<h1>Wait for admin approval.</h1>"
            else:
                return "<h1>Incorrect password</h1>"
        else:
            return "<h1> User not exists.</h1>"
    return render_template("login.html")


@app.route("/register_student" ,methods=["GET","POST"])
def register_student():
    if request.method== "POST":
        username=request.form.get("username")
        pd=request.form.get("pd")
        full_name=request.form.get("full_name")
        contact_info=request.form.get("contact_info")
        existing_user=User.query.filter_by(username=username).first()
        if existing_user:
            return "<h1> User already exists.</h1>"
        else:
            new_user = User(username=username, password=pd, role="student")
            new_student = Student(full_name=full_name, contact_info=contact_info)

            new_user.student_profile = new_student
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")

    return render_template("student_register.html")


@app.route("/register_company", methods=["GET", "POST"])
def register_company():
    if request.method == "POST":
        username = request.form.get("username")
        pd = request.form.get("pd")
        company_name = request.form.get("company_name")
        hr_contact = request.form.get("hr_contact")
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "<h1>Username already exists.</h1>"
        else:
            new_user=User(username=username,password=pd , role="company")
            new_company=Company(company_name=company_name, hr_contact=hr_contact)
            new_user.company_profile=new_company

            db.session.add(new_user)
            db.session.commit()
            
            return redirect("/login")

    return render_template("company_register.html")



