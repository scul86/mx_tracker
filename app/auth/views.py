from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from . import auth
from ..models import Vehicle
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        vehicle = Vehicle.query.filter_by(name=form.vehicle.data).first()
        if vehicle is not None and vehicle.verify_passwd(form.password.data):
            login_user(vehicle, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid login credentials')
    return render_template('auth/login.html', form=form)