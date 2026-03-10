from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from flask_migrate import Migrate

from config import DevelopmentConfig
import forms
from models import db, Alumnos

from . import alumnos
@alumnos.route("/alumnos/index")
@alumnos.route("/index")
def index():
	create_form = forms.UserForm2(request.form)
	alumno = Alumnos.query.all()
	return render_template("alumnos/index.html", form = create_form, alumno = alumno)

@alumnos.route("/alumnos", methods = ['GET', 'POST'])
def registrar():
	create_form = forms.UserForm2(request.form)
	if request.method == 'POST':
		alum = Alumnos(nombre = create_form.nombre.data, apellidos = create_form.apellidos.data, email = create_form.email.data, telefono = create_form.telefono.data)
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('alumnos.index'))
	return render_template("alumnos/alumnos.html", 
	form = create_form, alumno = alumnos)

@alumnos.route('/detalles', methods=['GET','POST'])
def detalles():
    create_form = forms.UserForm2(request.form)

    if request.method == 'GET':
        id = request.args.get('id')

        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        nombre = alum1.nombre
        apellidos = alum1.apellidos
        email = alum1.email
        telefono = alum1.telefono

        # cursos del alumno
        cursos = alum1.cursos

    return render_template(
        'alumnos/detalles.html',
        id=id,
        nombre=nombre,
        apellidos=apellidos,
        email=email,
        telefono=telefono,
        cursos=cursos
    )
@alumnos.route("/editar", methods=['GET', 'POST'])
def editar():
    create_form = forms.UserForm2(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = request.args.get('id')
        create_form.nombre.data = str.rstrip(alum1.nombre)
        create_form.apellidos.data = alum1.apellidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono

    if request.method == 'POST':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum1.id = id
        alum1.nombre = str.rstrip(create_form.nombre.data)
        alum1.apellidos = create_form.apellidos.data
        alum1.email = create_form.email.data
        alum1.telefono = create_form.telefono.data
        db.session.add(alum1)
        db.session.commit()
        return redirect(url_for('alumnos.index'))

    return render_template('alumnos/editar.html', form=create_form)

@alumnos.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
	create_form = forms.UserForm2(request.form)
	if request.method == 'GET':
		id = request.args.get('id')
		alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
		if alum1:
			create_form.id.data = alum1.id
			create_form.nombre.data = alum1.nombre
			create_form.apellidos.data = alum1.apellidos
			create_form.email.data = alum1.email
			create_form.telefono.data = alum1.telefono
			return render_template("alumnos/eliminar.html", form=create_form)
		
	if request.method == 'POST':
			id = create_form.id.data
			
			alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

			
			db.session.delete(alum1)
			db.session.commit()
			return redirect(url_for('alumnos.index'))
		
	return render_template("alumnos/eliminar.html", form=create_form)