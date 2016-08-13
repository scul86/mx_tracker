from app import app, db
from .models import Vehicle, GasStop
from .forms import AddGasStopForm
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required


@app.route('/')
@app.route('/index')
def index():
    return '<h1> Hello World</h1>'


@app.route('/vehicle/<name>')
@login_required
def vehicle(name):
    return '<h1>Hello, {}</h1>'.format(name)


@app.route('/add_gas_stop', methods=['GET', 'POST'])
@login_required
def add_gas_stop():
    form = AddGasStopForm()
    if form.validate_on_submit():
        vehicle = Vehicle.query.filter_by(name=form.vehicle.data).first()
        g = GasStop()
        g.gallons = form.gallons.data
        g.price = form.price.data
        g.trip = form.trip.data
        g.mpg = g.trip / g.gallons
        g.location = form.location.data
        g.vehicle_id = vehicle
        vehicle.add_mileage(g.trip)
        db.session.add(g)
        db.session.commit()
        flash('Record added')
        #TODO: fix the name arg in below line
        return redirect(request.args.get('next') or url_for('vehicle', name=vehicle.name))
    return render_template('add_gas_stop.html', form=form)