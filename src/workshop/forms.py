from wtforms import Form, StringField, TelField, validators

class NewClientForm(Form):
    first_name = StringField('First name', [validators.Length(min=3, max=30), validators.DataRequired()])
    last_name = StringField('Last name', [validators.Length(min=3, max=40), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=30), validators.Optional()])
    phone = TelField('Phone number', [validators.Length(min=9, max=9), validators.DataRequired()])
