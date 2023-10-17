from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import app, db, photos, bcrypt, login_manager
from flask_login import login_required, current_user, logout_user, login_user
from .forms import CustomerRegisterForm, CustomerLoginForm
from .model import Register
import secrets, os


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data, phone=form.phone.data, password=hash_password)
        db.session.add(register)
        flash(f'Welcome {form.username.data}. Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)


@app.route('/customer/login',  methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #login_user(user, form.remember.data)
            flash('You are login now!', 'success')
            #next = request.args.get('next')
            #return redirect(next or url_for('home'))
            return redirect(url_for('home'))
        flash('Incorrect email and password!', 'danger')
        return redirect(url_for('customerLogin'))    
    return render_template('customer/login.html', form=form) 
    

