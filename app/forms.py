from flask_wtf import Form
from wtforms import BooleanField, StringField, DecimalField, \
    SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length, Optional
from config import DATE_TIME_FORMAT
from .models import Vehicle


class AddGasStopForm(Form):
    choices = [(v.id, v.name) for v in Vehicle.query.all()]
    vehicle = SelectField('Vehicle',
                          choices=choices,
                          coerce=int)
    date = DateTimeField('Date (UTC)',
                         validators=[DataRequired()],
                         format=DATE_TIME_FORMAT,
                         description=DATE_TIME_FORMAT)
    location = StringField('Location',
                           validators=[DataRequired(), Length(1, 64)],
                           description='City, State')
    gallons = DecimalField('Gallons',
                           validators=[DataRequired()])
    price = DecimalField('Price per gallon',
                         validators=[DataRequired()])
    trip = DecimalField('Trip OD',
                        validators=[DataRequired()])
    tot = DecimalField('Vehicle OD',
                       validators=[Optional()],
                       description='Optional')
    correct_tot_mileage = BooleanField('Correct Vehicle Mileage')
    submit = SubmitField('Submit')