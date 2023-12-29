#Minden oldal, ahova a USER el tud jutni az ezen az oldalon kell megírnunk. Kivéve a Logint, mert azt az autentikációnál
from flask import Blueprint, render_template


#Ez Blueprint az applikációkhoz
Viewes = Blueprint('Views', __name__)


@Viewes.route('/') #Amikor ez kerül beírásra a URL-be, akkor erre weboldara hoz át. Majd ezután meghívja az alatta lévő funkciót.
def Home():
    return render_template("home.html")