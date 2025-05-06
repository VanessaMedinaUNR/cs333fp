from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


# Create an instance of the Flask class
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
      tasks = Todo.query.order_by(Todo.date_created).all()
      return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')

def delete(id):
    try:
            task_to_delete = Todo.query.get_or_404(id)
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/')
    except:
        return 'There was a problem deleting that task', 400


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    try:
        task = Todo.query.get(id)
        if not task:
            return 'There was an issue updating your task'
        if request.method == 'POST':
            task.content=request.form['content']
            db.session.commit()
            return redirect('/')
        else:
            return render_template('update.html', task = task)
    except:
        return 'There was an issue updating your task', 400
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

#small change