from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from workshop.models import Client
from workshop.forms import NewClientForm

def register_routes(app: Flask, db: SQLAlchemy) -> None:
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/client')
    def client_index():
        clients = db.session.execute(db.select(Client).order_by(Client.id)).scalars()
        return render_template('client/index.html', clients=clients)

    @app.route('/client/<int:id>')
    def client_show(id: int):
        client = db.get_or_404(Client, id)
        return render_template('client/show.html', client=client)

    @app.route('/client/new', methods=["GET", "POST"])
    def client_new():
        form = NewClientForm(request.form)
        print(form)
        print(form.first_name.id)
        if request.method == "POST" and form.validate():
            client = Client(
                    first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, phone_no=form.phone.data)
            db.session.add(client)
            db.session.commit()

            return redirect(url_for('client_show', id=client.id))
        return render_template("client/new.html", form=form)
