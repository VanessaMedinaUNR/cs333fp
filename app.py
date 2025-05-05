from flask import Flask, render_template, url_for

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
