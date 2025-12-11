from datetime import datetime
import json
from functools import reduce

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP

from workshop.forms import CarForm, ClientForm, JobForm
from workshop.models import Car, Client, Job, Maker, Model


def register_routes(app: Flask, db: SQLAlchemy) -> None:
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/client")
    def client_index():
        clients = db.session.execute(db.select(Client).order_by(Client.id)).scalars()
        return render_template("client/index.html", clients=clients)

    @app.route("/client/<int:id>")
    def client_show(id: int):
        client = db.get_or_404(Client, id)
        return render_template("client/show.html", client=client)

    @app.route("/client/<int:id>/edit", methods=["GET", "POST"])
    def client_edit(id: int):
        client = db.get_or_404(Client, id)
        form = ClientForm(request.form)

        if request.method == "POST":
            if form.validate():
                client.email = form.email.data
                client.full_name = form.full_name.data or ""
                client.phone = form.phone.data or ""
                db.session.add(client)
                db.session.commit()
                return redirect(url_for("client_show", id=client.id))

        form.email.data = client.email
        form.full_name.data = client.full_name
        form.phone.data = client.phone
        return render_template("client/new.html", client=client, form=form)

    @app.route("/client/new", methods=["GET", "POST"])
    def client_new():
        form = ClientForm(request.form)
        if request.method == "POST" and form.validate():
            client = Client(
                full_name=form.full_name.data,
                email=form.email.data,
                phone=form.phone.data,
            )
            db.session.add(client)
            db.session.commit()

            return redirect(url_for("client_show", id=client.id))
        return render_template("client/new.html", form=form)

    @app.route("/car")
    def car_index():
        cars = db.session.execute(db.select(Car).order_by(Car.plate)).scalars()
        return render_template("car/index.html", cars=cars)

    @app.route("/car/<int:id>")
    def car_show(id):
        car = db.get_or_404(Car, id)
        return render_template("car/show.html", car=car)

    @app.route("/car/<int:id>/edit", methods=["GET", "POST"])
    def car_edit(id):
        form = CarForm(request.form)
        form.maker_id.choices = [
            (m.id, m.name)
            for m in db.session.execute(db.select(Maker).order_by(Maker.name)).scalars()
        ]
        form.model_id.choices = [
            (m.id, m.name)
            for m in db.session.execute(db.select(Model).order_by(Model.name)).scalars()
        ]
        car = db.get_or_404(Car, id)
        if request.method == "POST" and form.validate():
            car.plate = form.plate.data or ""
            car.maker_id = form.maker_id.data
            car.model_id = form.model_id.data
            db.session.add(car)
            db.session.commit()
            return redirect(url_for("car_show", id=car.id))

        form.plate.data = car.plate
        form.maker_id.data = car.maker_id
        form.model_id.data = car.model_id

        return render_template("car/new.html", form=form, car=car, client=car.owner)

    @app.route("/car/<int:id>", methods=["POST"])
    def car_delete(id):
        car = db.get_or_404(Car, id)
        owner_id = car.owner.id
        db.session.delete(car)
        db.session.commit()
        return redirect(url_for("client_show", id=owner_id))

    @app.route("/client/<int:id>/car/new", methods=["GET", "POST"])
    def car_new(id):
        form = CarForm(request.form)
        form.maker_id.choices = [
            (m.id, m.name)
            for m in db.session.execute(db.select(Maker).order_by(Maker.name)).scalars()
        ]
        form.model_id.choices = [
            (m.id, m.name)
            for m in db.session.execute(db.select(Model).order_by(Model.name)).scalars()
        ]
        client = db.get_or_404(Client, id)
        if request.method == "POST" and form.validate():
            car = Car(
                owner_id=client.id,
                plate=form.plate.data,
                maker_id=form.maker_id.data,
                model_id=form.model_id.data,
            )
            db.session.add(car)
            db.session.commit()
            return redirect(url_for("client_show", id=client.id))
        return render_template("car/new.html", form=form, client=client)

    @app.route("/job/<int:id>")
    def job_show(id):
        job = db.get_or_404(Job, id)
        prices = json.loads(job.part_prices)
        parts_total = reduce(lambda sum, e: sum + e, prices, 0)
        return render_template(
            "job/show.html", job=job, prices=prices, parts_total=parts_total
        )

    @app.route("/job/<int:id>/edit", methods=["GET", "POST"])
    def job_edit(id):
        job = db.get_or_404(Job, id)
        form = JobForm(request.form)

        if request.method == "POST" and form.validate():
            # TODO: more fields
            job.description = form.description.data or ""
            job.work_price = float(form.work_price.data or 0)
            db.session.add(job)
            db.session.commit()
            return redirect(url_for("job_show", id=job.id))

        # TODO: add more
        form.description.data = job.description
        form.work_price.data = job.work_price

        return render_template("job/new.html", form=form, job=job, car=job.car)

    @app.route("/car/<int:id>/job/new", methods=["GET", "POST"])
    def job_new(id):
        car = db.get_or_404(Car, id)
        form = JobForm(request.form)

        if request.method == "POST" and form.validate():
            job = Job(
                car_id=car.id,
                description=form.description.data,
                work_price=form.work_price.data,
                date=datetime.now(),
                parts=[],
                part_prices="[]",
            )
            db.session.add(job)
            db.session.commit()
            return redirect(url_for("job_show", id=job.id))

        return render_template("job/new.html", form=form, car=car)

    @app.route("/job/<int:id>", methods=["POST"])
    def job_delete(id):
        job = db.get_or_404(Job, id)
        car_id = job.car_id
        db.session.delete(job)
        db.session.commit()
        return redirect(url_for("car_show", id=car_id))
