from flask import Flask, request, render_template , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/',methods=['POST','GET'])
def welcome():
    if request.method=='POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    alltodo = Todo.query.all()
    return render_template("welcome.html", alltodo = alltodo)

@app.route('/update/<int:sno>', methods=['POST','GET'])
def update(sno):
    if request.method=='POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo = todo)
    


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
     db.session.delete(todo)
     db.session.commit()
    else:
        return "todo doesn't exist"
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()   
    app.run(debug=True)