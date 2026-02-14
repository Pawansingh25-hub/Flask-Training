from flask import Flask, render_template # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
db=SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    role = db.Column(db.String(20))


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@app.route("/add")
def add():
    admin = user(name = "pawan", role = "admin")
    db.session.add(admin)
    db.session.commit()

    return "<p>Data Added</p>"




@app.route("/show")
def show():
   users = user.query.all()  # Fixed: lowercase 'user' and 'users'
   output = ""
   for usr in users:  # Fixed: lowercase 'usr'
       print(usr.name)  # Fixed: correct variable name and proper indentation
       output += f"<p>{usr.name} - {usr.role}</p>"  # Optional: build output to display

   return output if output else "<p>No users found</p>"




@app.route("/delete/<name>")
def delete(name):
    user_to_delete = user.query.filter_by(name=name).first()
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return f"<p>User '{name}' deleted successfully</p>"
    else:
        return f"<p>User '{name}' not found</p>"
    
@app.route("/show_all")
def show_all():
   student = user.query.all()  # Fixed: lowercase 'user' and 'users'
   
   return render_template('index.html', user = student)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)