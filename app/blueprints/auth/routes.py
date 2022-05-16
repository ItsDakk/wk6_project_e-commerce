from flask import render_template, request, flash, url_for, redirect
from . forms import EditProfileForm, LoginForm, RegisterForm
from . import bp as auth
from app.models import User
from flask_login import current_user, logout_user, login_user, login_required
from werkzeug.security import check_password_hash

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method =='POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        customer = User.query.filter_by(email=email).first()
        if customer and check_password_hash(customer.password, password):
            login_user(customer)
            flash('Welcome back!', 'success')
            return redirect(url_for('main.index'))
        flash("Doesn't look like you typed that in right.", 'danger')
        return render_template('login.html.j2', form = form)
    return render_template('login.html.j2', form = form)

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method =='POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data,
                "password": form.password.data
            }

            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
            
        except:
            flash("Whoops! Looks like there was an unexpected error on our end. Please try again later!", 'danger')
            return render_template('register.html.j2', form = form)
        flash(f"Welcome!", 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html.j2', form = form)

@auth.route('/edit_prof', methods=['GET', 'POST'])
def edit_prof():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data = {
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data,
                "password": form.password.data
            }  
        user = User.query.filter_by(email = new_user_data['email']).first()
        if user and user.email != current_user.email:
            flash ('Email is already in use', 'danger')
            return redirect(url_for('auth.edit_prof'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile Successfully Updated', 'success')
        except:
            flash('There seems to have been an unexpected error. Please try again', 'danger')
            return redirect(url_for('auth.edit_profile'))
        return redirect(url_for('main.index'))
    return render_template('register.html.j2', form = form)

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'warning')
        return redirect(url_for('auth.login'))