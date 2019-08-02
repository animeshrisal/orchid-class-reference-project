from flask import Flask
import os

app = Flask(__name__)

if __name__  == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
