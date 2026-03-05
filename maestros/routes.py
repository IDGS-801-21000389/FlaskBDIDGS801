from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from flask_migrate import Migrate

from config import DevelopmentConfig
import forms
from models import db, Maestros

from . import maestros

@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"perfil de {nombre}"

@maestros.route("/listadoMaes")
def listadoMaes():
	create_form = forms.UserForm(request.form)
	maestros = Maestros.query.all()
	return render_template("maestros/listadoMaes.html", form = create_form, maestros = maestros)

@maestros.route("/maestros/agregar", methods = ['GET', 'POST'])
def agregar():
	create_form = forms.UserForm(request.form)
	if request.method == 'POST':
		maes = Maestros(nombre = create_form.nombre.data, apellidos = create_form.apellidos.data, especialidad = create_form.especialidad.data, email = create_form.email.data)
		db.session.add(maes)
		db.session.commit()
		return redirect(url_for('maestros.listadoMaes'))
	return render_template("maestros/agregar.html", 
	form = create_form, alumno = maestros)

@maestros.route('/maestros/detalles', methods = ['GET', 'POST'])
def detallesMaes():
	create_form = forms.UserForm(request.form)
	if request.method == 'GET':
		matricula = request.args.get('matricula')
		maestros1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
		matricula = request.args.get('matricula')
		nombre = maestros1.nombre
		apellidos = maestros1.apellidos
		especialidad = maestros1.especialidad
		email = maestros1.email
		
	return render_template('maestros/detalles.html', matricula = matricula, nombre = nombre, apellidos = apellidos, especialidad = especialidad, email = email)

@maestros.route("/maestros/editar", methods=['GET', 'POST'])
def editarMaes():
    create_form = forms.UserForm(request.form)

    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestros1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        create_form.matricula.data = request.args.get('matricula')
        create_form.nombre.data = str.rstrip(maestros1.nombre)
        create_form.apellidos.data = maestros1.apellidos
        create_form.especialidad.data = maestros1.especialidad
        create_form.email.data = maestros1.email

    if request.method == 'POST':
        matricula = request.args.get('matricula')
        maestros1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        maestros1.matricula = request.args.get('matricula')
        maestros1.nombre = str.rstrip(create_form.nombre.data)
        maestros1.apellidos = create_form.apellidos.data
        maestros1.especialidad = create_form.especialidad.data
        maestros1.email = create_form.email.data

        db.session.add(maestros1)
        db.session.commit()

        return redirect(url_for('maestros.listadoMaes'))

    return render_template('maestros/editar.html', form=create_form)

@maestros.route("/maestros/eliminar", methods=['GET', 'POST'])
def eliminarMaes():
	create_form = forms.UserForm(request.form)
	if request.method == 'GET':
		matricula = request.args.get('matricula')
		maestros1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
		if maestros1:
			create_form.matricula.data = maestros1.matricula
			create_form.nombre.data = maestros1.nombre
			create_form.apellidos.data = maestros1.apellidos
			create_form.especialidad.data = maestros1.especialidad
			create_form.email.data = maestros1.email
			return render_template("maestros/eliminar.html", form=create_form)
		
	if request.method == 'POST':
			matricula = create_form.matricula.data
			
			maestros = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()

			db.session.delete(maestros)
			db.session.commit()
			return redirect(url_for('maestros.listadoMaes'))
		
	return render_template("maestros/eliminar.html", form=create_form)