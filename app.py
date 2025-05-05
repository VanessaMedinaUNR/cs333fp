from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

# Create an instance of the Flask class
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed= db.Column(db.Integer, default =0)

    def __repr__(self):
        return '<Task %r>' % self.id

# Define a route for the home page
@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
