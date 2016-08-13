from app import app, db
from .models import Vehicle, GasStop
from .forms import AddGasStopForm
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_required


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/vehicle/<name>')
@login_required
def vehicle(name):
    v = Vehicle.query.filter_by(name=name).first()
    if not v:
        abort(404)
    stops = v.gas_stop.all()
    return render_template('vehicle.html', vehicle=v, stops=stops)


@app.route('/add_gas_stop', methods=['GET', 'POST'])
@login_required
def add_gas_stop():
    form = AddGasStopForm()
    if form.validate_on_submit():
        v = Vehicle.query.filter_by(name=form.vehicle.data).first()
        if v is not None and v.is_authenticated:
            print('Authenticated {}'.format(v))
            stop = GasStop()
            stop.gallons = form.gallons.data
            stop.price = form.price.data
            stop.trip = form.trip.data
            stop.mpg = stop.trip / stop.gallons
            stop.location = form.location.data
            stop.vehicle_id = v.id
            v.add_mileage(stop.trip)
            db.session.add(stop)
            db.session.commit()
            flash('Record added')
            return redirect(request.args.get('next') or url_for('vehicle', name=v.name))
        flash('Invalid Vehicle')
        return  redirect(url_for('add_gas_stop'))
    return render_template('add_gas_stop.html', form=form)