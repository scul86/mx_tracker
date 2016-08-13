from flask_wtf import Form
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length


class AddGasStopForm(Form):
    vehicle = StringField('Vehicle', validators=[DataRequired(), Length(1, 64)])
    location = StringField('Location', validators=[DataRequired(), Length(1, 64)])
    gallons = DecimalField('Gallons', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    trip = DecimalField('Trip OD', validators=[DataRequired()])
    tot = DecimalField('Vehicle OD')
    submit = SubmitField('Submit')