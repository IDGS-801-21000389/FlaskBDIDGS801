from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()

class Alumnos(db.model):
    __tablename__ = 'alumnos'
    id=db.column(db.integer, primary_key=True)
    nombre = db.column(db.String(50))
    apaterno = db.column(db.String(50))
    email = db.column(db.String(50))
    created_date = db.Column(db.DateTime, default = datetime.datetime.now)

