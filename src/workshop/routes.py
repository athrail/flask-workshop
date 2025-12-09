from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

def register_routes(app: Flask, db: SQLAlchemy) -> None:

    @app.route('/')
    def index():
        return render_template('index.html')

