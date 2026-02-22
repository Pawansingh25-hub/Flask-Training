from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from models import db, Admin, Job, Application

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "mysecretkey"

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin_login"

@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))

with app.app_context():
    db.create_all()
    

@app.route("/")
def index():
    jobs = Job.query.all()
    return render_template("index.html", jobs=jobs)


@app.route("/apply/<int:job_id>", methods=["GET", "POST"])
def apply(job_id):
    job = Job.query.get_or_404(job_id)

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        new_app = Application(name=name, email=email, phone=phone, job_id=job_id)
        db.session.add(new_app)
        db.session.commit()

        flash("Application Submitted Successfully!", "success")
        return redirect(url_for("index"))

    return render_template("apply.html", job=job)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(username=username, password=password).first()

        if admin:
            login_user(admin)
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid Username or Password!", "danger")

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    jobs = Job.query.all()
    return render_template("admin_dashboard.html", jobs=jobs)


@app.route("/admin/add_job", methods=["GET", "POST"])
@login_required
def add_job():
    if request.method == "POST":
        title = request.form["title"]
        company = request.form["company"]
        location = request.form["location"]
        description = request.form["description"]

        new_job = Job(title=title, company=company, location=location, description=description)
        db.session.add(new_job)
        db.session.commit()

        flash("Job Added Successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("add_job.html")


@app.route("/admin/applications")
@login_required
def applications():
    apps = Application.query.all()
    return render_template("applications.html", apps=apps)


@app.route("/admin/update_status/<int:app_id>", methods=["POST"])
@login_required
def update_status(app_id):
    app_data = Application.query.get_or_404(app_id)
    app_data.status = request.form["status"]

    db.session.commit()
    flash("Status Updated Successfully!", "success")

    return redirect(url_for("applications"))


@app.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for("admin_login"))


if __name__ == "__main__":
    app.run(debug=True)
