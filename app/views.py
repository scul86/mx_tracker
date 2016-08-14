from app import app, db
from .models import Vehicle, GasStop
from .forms import AddGasStopForm
from flask import render_template, redirect, \
    request, url_for, flash, abort, g
from flask_login import login_required, current_user
from config import DATE_FORMAT, POSTS_PER_PAGE


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
    # stops = v.gas_stop.all()
    stops = v.gas_stop.order_by(GasStop.timestamp.asc()).paginate(page_num, POSTS_PER_PAGE, False)
    return render_template('vehicle.html', vehicle=v,
                           stops=stops, DATE_FORMAT=DATE_FORMAT)


@app.route('/add_gas_stop', methods=['GET', 'POST'])
@login_required
def add_gas_stop():
    form = AddGasStopForm(vehicle=g.vehicle.name)
    if form.validate_on_submit():
        vehicle = Vehicle.query.get(form.vehicle.data)
        if vehicle is not None and vehicle.is_authenticated:
            stop = GasStop()
            stop.gallons = form.gallons.data
            stop.price = form.price.data
            stop.trip = form.trip.data
            stop.mpg = stop.trip / stop.gallons
            stop.location = form.location.data
            stop.timestamp = form.date.data
            stop.vehicle_id = vehicle.id
            vehicle.add_mileage(stop.trip)
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