import json
from functools import reduce

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from workshop.models import Client, Job, Maker, Model, Car
from workshop.forms import NewCarForm, NewClientForm


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

    @app.route("/client/new", methods=["GET", "POST"])
    def client_new():
        form = NewClientForm(request.form)
        if request.method == "POST" and form.validate():
            client = Client(
                full_name=form.full_name.data,
                email=form.email.data,
                phone_no=form.phone.data,
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

    @app.route("/car/<int:id>", methods=["POST"])
    def car_delete(id):
        car = db.get_or_404(Car, id)
        owner_id = car.owner.id
        db.session.delete(car)
        db.session.commit()
        return redirect(url_for("client_show", id=owner_id))

    @app.route("/client/<int:id>/car/new", methods=["GET", "POST"])
    def car_new(id):
        form = NewCarForm(request.form)
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
        return render_template("car/new.html", form=form, client_id=client.id)

    @app.route("/job/<int:id>")
    def job_show(id):
        job = db.get_or_404(Job, id)
        prices = json.loads(job.part_prices)
        parts_total = reduce(lambda sum, e: sum + e, prices)
        return render_template(
            "job/show.html", job=job, prices=prices, parts_total=parts_total
        )

    @app.route("/job/<int:id>", methods=["POST"])
    def job_delete(id):
        job = db.get_or_404(Job, id)
        car_id = job.car_id
        db.session.delete(job)
        db.session.commit()
        return redirect(url_for("car_show", id=car_id))
