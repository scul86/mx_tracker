from flask_wtf import Form
from wtforms import StringField, DecimalField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length
from config import DATE_FORMAT
from datetime import datetime


class AddGasStopForm(Form):
    vehicle = StringField('Vehicle', validators=[DataRequired(), Length(1, 64)])
    date = DateTimeField('Date (UTC)', validators=[DataRequired()], format=DATE_FORMAT, default=datetime.utcnow())
    location = StringField('Location', validators=[DataRequired(), Length(1, 64)])
    gallons = DecimalField('Gallons', validators=[DataRequired()])
    price = DecimalField('Price per gallon', validators=[DataRequired()])
    trip = DecimalField('Trip OD', validators=[DataRequired()])
    tot = DecimalField('Vehicle OD')
    submit = SubmitField('Submit')