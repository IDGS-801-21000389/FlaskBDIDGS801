from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from maestros.routes import maestros
from alumnos.routes import alumnos
from flask_migrate import Migrate

from config import DevelopmentConfig
import forms
from models import db


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(alumnos)
app.register_blueprint(maestros)

csrf = CSRFProtect()
db.init_app(app)
migrate = Migrate(app, db)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.route("/")
@app.route("/index2")
def index2():
	return render_template('index2.html')

if __name__ == '__main__':
	csrf.init_app(app)
	app.run(debug=True, port=5070)

