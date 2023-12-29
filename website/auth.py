from flask import Blueprint


#Ez Blueprint az applikációkhoz
Auth = Blueprint('Auth', __name__)

@Auth.route("/login")
def Login():
    return "<p>Login</>"

@Auth.route('/logout')
def Logout():
    return "<p>Logout</>"

@Auth.route("/sign-up")
def SignUp():
    return "<p>Sign Up</p>"