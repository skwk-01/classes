from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    times = db.Column(db.Integer)
    cnt = db.Column(db.Integer, default=0)

@app.route("/", methods=["GET", "POST"])
def home():
    subjects = Subject.query.all()
    return render_template("index.html", subjects=subjects)


@app.route('/add', methods=["POST"])
def add():
    title = request.form.get("title")
    times = request.form.get("times")
    newsub = Subject(title=title, times=times, cnt=0)
    db.session.add(newsub)
    db.session.commit()
    return redirect(url_for("setting"))

@app.route('/do/<int:sub_id>', methods=["POST"])
def do(sub_id):
    subject = Subject.query.filter_by(id=sub_id).first()
    if subject:
        subject.cnt += 1
        db.session.commit()
    return redirect(url_for("home"))

@app.route('/undo/<int:sub_id>', methods=["POST"])
def undo(sub_id):
    subject = Subject.query.filter_by(id=sub_id).first()
    if subject:
        subject.cnt -= 1
        db.session.commit()
    return redirect(url_for("home"))

@app.route("/setting")
def setting():
    subjects = Subject.query.all()
    return render_template("setting.html", subjects=subjects)

@app.route("/setting/delete/<int:sub_id>", methods=["POST"])
def delete(sub_id):
    subject = Subject.query.filter_by(id=sub_id).first()
    if subject:
        db.session.delete(subject)
        db.session.commit()
    return redirect(url_for("setting"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
