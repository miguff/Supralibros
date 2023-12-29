from flask import Flask

def CreateApp():
    App = Flask(__name__)
    App.config['SECRET_KEY'] = 'bfiebfolibvfruuevuruvr3uvfuv' #Eltárolja a Session és Cookie adatokat

    #A Route-okat, amiket létrehozunk az Views fülön, azokat itt meg kell adni neki, hogy tudja, hogy hogyan kezelni
    from .views import Viewes
    from .auth import Auth

    #Ezek lesznek a prefix-jei az URL-nek és utána jönnek azok, amik a views résznél megvannak adva
    App.register_blueprint(Viewes, url_prefix="/")
    App.register_blueprint(Auth, url_prefix="/") 

    return App