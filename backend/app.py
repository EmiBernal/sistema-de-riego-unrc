import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__,
    template_folder="/frontend/templates",
    static_folder="/frontend/static",
)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

db = SQLAlchemy(app)

@app.get("/")
def index():
    return render_template("index.html")