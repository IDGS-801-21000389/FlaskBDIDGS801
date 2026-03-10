from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from flask_migrate import Migrate

from config import DevelopmentConfig
import forms
from models import Alumnos, Inscripcion, Maestros, db, Cursos

from . import cursos

@cursos.route("/listaCurso")
def listaCurso():
	create_form = forms.UserFormC(request.form)
	cursos = Cursos.query.all()
	return render_template("cursos/listaCurso.html", form = create_form, cursos = cursos)

@cursos.route("/cursos/agregarCurso", methods=['GET','POST'])
def agregarCurso():

    create_form = forms.UserFormC(request.form)

    maestros_lista = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, m.nombre) for m in maestros_lista]

    if request.method == 'POST':

        curso = Cursos(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=create_form.maestro_id.data
        )

        db.session.add(curso)
        db.session.commit()

        return redirect(url_for('cursos.listaCurso'))

    return render_template("cursos/agregarCurso.html", form=create_form)

@cursos.route('/cursos/detallesCurso')
def detallesCurso():

    id = request.args.get('id')

    curso = db.session.query(Cursos).filter(Cursos.id == id).first()

    # alumnos que ya están inscritos
    inscritos_ids = [a.id for a in curso.alumnos]

    # alumnos disponibles para inscribir
    alumnos = db.session.query(Alumnos).filter(
        ~Alumnos.id.in_(inscritos_ids)
    ).all()

    return render_template(
        'cursos/detallesCurso.html',
        curso=curso,
        alumnos=alumnos
    )

@cursos.route("/cursos/editarCurso", methods=['GET','POST'])
def editarCurso():

    create_form = forms.UserFormC(request.form)

    maestros_lista = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, m.nombre) for m in maestros_lista]

    if request.method == 'GET':

        id = request.args.get('id')

        curso = db.session.query(Cursos).filter(Cursos.id == id).first()

        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id

    if request.method == 'POST':

        id = create_form.id.data

        curso = db.session.query(Cursos).filter(Cursos.id == id).first()

        curso.nombre = create_form.nombre.data
        curso.descripcion = create_form.descripcion.data
        curso.maestro_id = create_form.maestro_id.data

        db.session.add(curso)
        db.session.commit()

        return redirect(url_for('cursos.listaCurso'))

    return render_template("cursos/editarCurso.html", form=create_form)

@cursos.route("/cursos/eliminarCurso", methods=['GET','POST'])
def eliminarCurso():

    create_form = forms.UserFormC(request.form)

    if request.method == 'GET':

        id = request.args.get('id')

        curso = db.session.query(Cursos).filter(Cursos.id == id).first()

        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion

        return render_template("cursos/eliminarCurso.html", form=create_form)

    if request.method == 'POST':

        id = create_form.id.data

        curso = db.session.query(Cursos).filter(Cursos.id == id).first()

        db.session.delete(curso)
        db.session.commit()

        return redirect(url_for('cursos.listaCurso'))
    
@cursos.route('/cursos/inscribir', methods=['POST'])
def inscribir():

    alumno_id = request.form.get('alumno_id')
    curso_id = request.form.get('curso_id')

    inscripcion = Inscripcion(
        alumno_id=alumno_id,
        curso_id=curso_id
    )

    db.session.add(inscripcion)
    db.session.commit()

    return redirect(url_for('cursos.detallesCurso', id=curso_id))

@cursos.route('/cursos/quitarAlumno')
def quitarAlumno():

    alumno_id = request.args.get('alumno')
    curso_id = request.args.get('curso')

    inscripcion = db.session.query(Inscripcion).filter(
        Inscripcion.alumno_id == alumno_id,
        Inscripcion.curso_id == curso_id
    ).first()

    if inscripcion:
        db.session.delete(inscripcion)
        db.session.commit()

    return redirect(url_for('cursos.detallesCurso', id=curso_id))