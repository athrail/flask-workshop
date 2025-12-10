from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    SelectField,
    StringField,
    TelField,
    validators,
)


class NewClientForm(FlaskForm):
    full_name = StringField(
        "Full name", [validators.Length(min=3, max=40), validators.DataRequired()]
    )
    email = StringField(
        "Email Address", [validators.Length(min=6, max=30), validators.Optional()]
    )
    phone = TelField(
        "Phone number", [validators.Length(min=9, max=9), validators.DataRequired()]
    )


class NewCarForm(FlaskForm):
    plate = StringField(
        "License plate", [validators.Length(min=3, max=15), validators.DataRequired()]
    )
    owner_id = IntegerField("Owner", [validators.DataRequired()])
    maker_id = SelectField("Maker", [validators.DataRequired()], coerce=int)
    model_id = SelectField("Model", [validators.DataRequired()], coerce=int)
