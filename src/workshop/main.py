def create_app():
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_wtf import CSRFProtect

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.root_path}/workshop.db"
    app.config["SECRET_KEY"] = "do not use this for prod!"

    from workshop.models import Base

    db = SQLAlchemy(model_class=Base)
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
    csrf = CSRFProtect()
    csrf.init_app(app)

    from workshop.routes import register_routes

    register_routes(app, db)

    return app


def main():
    app = create_app()
    app.run()
