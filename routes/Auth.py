from flask import request, Blueprint, render_template, url_for, session, redirect

import uuid, time

from core import JsonResponse
from core import Database
from core import Config
from core import Authorization
from core import Security

from model.Staff import Staff as StaffModel
from model.PasswordReset import PasswordReset as PasswordResetModel

Auth = Blueprint('Auth', __name__)

@Auth.route('/auth/login', methods=['GET'])
def Login():
    """ Example route, show information about system and current session. """
    if Authorization.isLoggedIn(session.get('user')):
        return redirect( url_for('Campus.List') )

    return render_template('auth/login.html')

@Auth.route('/auth/login', methods=['POST'])
def LoginPost():
    """ Example route, show information about system and current session. """
    if Authorization.isLoggedIn(session.get('user')):
        return redirect( url_for('Campus.List') )
    
    email = request.form.get('email')
    password = request.form.get('password')

    staff = StaffModel.findBy('email', email)

    if len(staff) != 0:
        staff = staff[0]
        if staff.getPassword() == Security.hashPassword(password, staff.getSalt()):
            session['user'] = staff.getId()
            return redirect( url_for('Campus.List') )

    return render_template('auth/login.html', data = {
        'email': email
    })

@Auth.route('/auth/logout', methods=['GET'])
def Logout():
    session['user'] = None
    return redirect( url_for('Auth.Login') )

@Auth.route('/auth/password-reset', methods=['GET'])
def PasswordReset():
    if Authorization.isLoggedIn(session.get('user')):
        return redirect( url_for('Campus.List') )

    return render_template('auth/password_reset.html', data = {

    })

@Auth.route('/auth/password-reset', methods=['POST'])
def PasswordResetPost():
    if Authorization.isLoggedIn(session.get('user')):
        return redirect( url_for('Campus.List') )
    
    email = request.form.get('email')

    staff = StaffModel.findby('email', email)

    if len(staff) != 0:
        resetToken = str(uuid.uuid4()).replace('-', '')
        expires = time.time() + 30*60 # 30 minutes

        prm = PasswordResetModel()

        prm.setToken(resetToken) \
           .setUserId(staff.getId()) \
           .setUserType('staff') \
           .setExpires(expires) \
           .save()

        Email.sendEmail(email, 'password_reset', {'password_reset_url': Config.getValue('APP_URL') + '/auth/password-reset/' + resetToken})

    return render_template('auth/password_reset_sent.html')

@Auth.route('/auth/password-reset/<token>')
def PasswordResetConfirm(token):
    if Authorization.isLoggedIn(session.get('user')):
        return redirect( url_for('Campus.List') )

    return render_template('auth/password_reset_confirm.html', data = {

    })