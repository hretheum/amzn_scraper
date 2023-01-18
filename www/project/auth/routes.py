from flask import render_template, session, redirect, url_for, request, get_flashed_messages, flash
from werkzeug.security import check_password_hash
from www.project.models import User
from www.project.auth import auth_bp
from www.project import db


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        messages = get_flashed_messages()
        return render_template('login.html', messages=messages)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = db.session.query(User).filter(User.username == username).first()

        if user_data:
            hashed_password = user_data.password_hash
            if check_password_hash(hashed_password, password):
                session['public_id'] = user_data.public_id
                session['username'] = user_data.username
                return redirect('/')

        flash('błędne dane logowania')
        return redirect(url_for('auth_endpoints.login'))


@auth_bp.route('logout')
def logout():
    session.clear()
    return redirect(url_for('auth_endpoints.login'))