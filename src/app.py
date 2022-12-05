#!/usr/bin/env python
import flask

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)     # open for everyone