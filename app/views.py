from app import app, db, set_pickled_decimal
from .models import Vehicle, GasStop
from .forms import AddGasStopForm
from flask import render_template, redirect, \
    request, url_for, flash, abort, g
from flask_login import login_required, current_user
from datetime import datetime

from config import DATE_FORMAT, POSTS_PER_PAGE

import pickle


@app.before_request
def before_request():
    g.vehicle = current_user


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/vehicle/<name>')
@app.route('/vehicle/<name>/<int:page_num>')
@login_required
def vehicle(name, page_num=1):
    v = Vehicle.query.filter_by(name=name).first()
    if not v:
        abort(404)
    if not v.total_mileage:
        v.set_mileage(0)
    stops = v.gas_stop.order_by(GasStop.timestamp.desc()).\
              paginate(page_num, POSTS_PER_PAGE, False)
    return render_template('vehicle.html', vehicle=v,
                           stops=stops, DATE_FORMAT=DATE_FORMAT, loads=pickle.loads)


@app.route('/add_gas_stop', methods=['GET', 'POST'])
@login_required
def add_gas_stop():
    form = AddGasStopForm(date=datetime.utcnow())
    form.vehicle.choices = [(v.id, v.name) for v in Vehicle.query.all()]
    form.vehicle.data = g.vehicle.id
    form.vehicle.coerce = int
    if form.validate_on_submit():
        vehicle = Vehicle.query.get(form.vehicle.data)
        if vehicle is not None and vehicle.is_authenticated and vehicle.id == g.vehicle.id:
            stop = GasStop()
            stop.gallons = set_pickled_decimal(form.gallons.data)
            stop.price = set_pickled_decimal(form.price.data)
            stop.trip = set_pickled_decimal(form.trip.data)
            stop.mpg = set_pickled_decimal(form.trip.data / form.gallons.data)
            stop.location = form.location.data
            stop.timestamp = form.date.data
            stop.vehicle_id = vehicle.id
            vehicle.add_mileage(form.trip.data)
            if form.correct_tot_mileage.data and form.tot.data:
                vehicle.set_mileage(form.tot.data)
                flash('Vehicle mileage corrected')
            elif form.correct_tot_mileage.data and not form.tot.data:
                flash('Notice: Vehicle mileage not corrected')
            db.session.add(stop)
            db.session.commit()
            flash('Record added')
            return redirect(request.args.get('next') or
                            url_for('vehicle', name=vehicle.name))
        flash('Invalid Vehicle')
        return redirect(url_for('add_gas_stop'))
    return render_template('add_gas_stop.html', form=form)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    stop = GasStop.query.get(id)
    if stop is None:
        flash('Not found')
        return redirect(url_for('vehicle', name=g.vehicle.name))
    if stop.vehicle.id != g.vehicle.id:
        flash('You can\'t delete that stop')
        return redirect(url_for('vehicle', name=g.vehicle.name))
    db.session.delete(stop)
    db.session.commit()
    flash('Gas stop deleted')
    return redirect(url_for('vehicle', name=g.vehicle.name))

# TODO: add the html files
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template('server_error.html'), 500
