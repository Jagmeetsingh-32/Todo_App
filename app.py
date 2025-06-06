from flask import Flask, render_template, request,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)  # Increased length
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Create database tables within app context
with app.app_context():
    db.create_all()
    print("DAtabase bn gya")

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        
        title= request.form['title']
        
        desc= request.form['desc']
        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template('hello.html',allTodo=allTodo)  # Changed to index.html as more standard

@app.route('/show')
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/update/<int:sno>' , methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        
        title= request.form['title']
        desc= request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    allTodo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',allTodo=allTodo)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    allTodo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)