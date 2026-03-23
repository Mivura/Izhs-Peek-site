#import os
#import sys
#sys.path.append('/home/c/cv66083/venv/lib/python3.12/site-packages/')
from flask import Flask
app = Flask(__name__)
application = app
@app.route('/')
def hello_world():
    return 'Hello, World!'
if __name__ == '__main__':
    app.run()
