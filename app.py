# Dependencies  and set-up
from flask import Flask

# Instantiate Flask
app = Flask(__name__)

# Create the index route
@app.route('/')
def index():
    print('Server received request for index page')
    return '''
    Welcome to the index page. \n
    The following routes are available: \n
    <a href="/about">About</a> \n
    <a href="/contact">Contact</a>
    '''
# Create the about route
@app.route('/api/v1.0/precipitation')
def about():
    print('Server received request for about page')
    return 'This is the about page <a href="../">Home</a>'
# Create the contact route
@app.route('/contact')
def contact():
    print('Server received request for contact page')
    return '''
    This is the contact page \n
    <a href="../">Home</a>
    '''

if __name__ == "__main__":
    app.run(debug=True)
