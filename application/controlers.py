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


@app.route("/admin_dashboard" )
def admin():
    pending_companies= Company.query.filter_by(is_approved=False , is_blacklisted=False).all()
    approved_companies=Company.query.filter_by(is_approved=True , is_blacklisted=False).all()
    all_students=Student.query.filter_by( is_blacklisted=False).all()
    ongoing_drives = PlacementDrive.query.filter_by(status='Pending').all()
    student_applications = Application.query.filter_by(status='Applied').all()

    total_companies = len(approved_companies)
    total_students = len(all_students)
    total_drives = len(ongoing_drives)
    total_apps = len(student_applications)
    return render_template( "admin_dashboard.html", pending_companies=pending_companies,approved_companies=approved_companies,
        all_students=all_students,
        ongoing_drives=ongoing_drives,
        student_applications=student_applications,
        total_companies=total_companies,
        total_students=total_students,
        total_drives=total_drives,
        total_apps=total_apps
    )
@app.route("/approve_company/<int:id>")
def approve_company(id):
    this_company=Company.query.get(id)

    if this_company:
        this_company.is_approved= True
        db.session.commit()

    return redirect("/admin_dashboard")

@app.route("/reject_company/<int:id>")
def reject_company(id):
    this_company=Company.query.get(id)
    if this_company:
        this_user=User.query.get(this_company.user_id)
        db.session.delete(this_company)
        if this_user:
            db.session.delete(this_user)

    return redirect("/admin_dashboard")

@app.route("/blacklist_company/<int:id>")
def blacklist_company(id):
    this_company=Company.query.get(id)

    if this_company:
        this_company.is_approved=False
        this_company.is_blacklisted = True
        db.session.commit()
    return redirect("/admin_dashboard")

@app.route("/blacklist_student/<int:id>")
def blacklist_student(id):
    this_student=Student.query.get(id)

    if this_student:
        this_student.is_blacklisted=True
        db.session.commit()
    return redirect("/admin_dashboard")

@app.route("/")
def home():
    return redirect("/login")

@app.route("/complete_drive/<int:id>")
def complete_drive(id):
    this_drive=PlacementDrive.query.get(id)

    if this_drive:
        this_drive.status = 'Completed'
        db.session.commit()
    return redirect("/admin_dashboard")