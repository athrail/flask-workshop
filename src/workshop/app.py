def create_app():
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    from workshop.routes import register_routes
    register_routes(app, db)

    return app

def main():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()
