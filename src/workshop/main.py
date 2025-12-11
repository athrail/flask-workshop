from flask_sqlalchemy import SQLAlchemy


def create_app():
    from flask import Flask
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


def populate_fake_data():
    from flask import Flask
    from flask_migrate import Migrate
    from faker import Faker
    from workshop.models import (
        Base,
        Client,
        Maker,
        Model,
        Car,
        Job,
        Part,
        Producer,
        job_part_association_table,
    )
    from random import choice
    from sqlalchemy import Table

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.root_path}/workshop.db"

    def clear_table_for_model(db: SQLAlchemy, model):
        table = Table(model.__tablename__, model.metadata)
        db.session.execute(table.delete())

    with app.app_context():
        db = SQLAlchemy(model_class=Base)
        db.init_app(app)

        db.create_all()
        migrate = Migrate()
        migrate.init_app(app, db)

        fake = Faker()
        Faker.seed(123456789)

        clear_table_for_model(db, Client)
        clients = [
            Client(full_name=fake.name(), email=fake.email(), phone=fake.phone_number())
            for _ in range(3)
        ]
        db.session.add_all(clients)

        clear_table_for_model(db, Maker)
        makers = [Maker(name=name) for name in ["FSO", "Skoda", "Ford", "Opel"]]
        db.session.add_all(makers)

        clear_table_for_model(db, Model)
        models = [
            Model(
                name=fake.word(),
                production_start=fake.year(),
                production_end=int(fake.year()) + 10,
                maker=choice(makers),
            )
            for _ in range(5)
        ]
        db.session.add_all(models)

        clear_table_for_model(db, Car)
        cars = [
            Car(
                plate=fake.license_plate(),
                owner=choice(clients),
                maker=choice(makers),
                model=choice(models),
            )
            for _ in range(10)
        ]
        db.session.add_all(cars)

        clear_table_for_model(db, Producer)
        producers = [Producer(name=fake.company()) for _ in range(10)]
        db.session.add_all(producers)

        clear_table_for_model(db, Part)
        parts = [
            Part(
                name="Some part name",
                number=fake.random_number(10),
                producer=choice(producers),
            )
            for _ in range(50)
        ]
        db.session.add_all(parts)

        db.session.execute(job_part_association_table.delete())
        clear_table_for_model(db, Job)
        jobs = [
            Job(
                description=fake.sentence(10),
                car=choice(cars),
                parts=fake.random_sample(parts, length=5),
            )
            for _ in range(10)
        ]
        db.session.add_all(jobs)

        db.session.commit()


def main():
    app = create_app()
    app.run()
