from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# =========================
# TABLA INSCRIPCION (Muchos a Muchos)
# =========================
class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'
    
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    
    # Evita inscripciones duplicadas
    __table_args__ = (
        db.UniqueConstraint('alumno_id', 'curso_id', name='unique_inscripcion'),
    )


# =========================
# ALUMNOS
# =========================
class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    email = db.Column(db.String(120))
    telefono = db.Column(db.String(20))
    created_date = db.Column(
        db.DateTime,
        default=datetime.datetime.now
    )
    
    # Relación muchos a muchos con cursos
    cursos = db.relationship(
        'Cursos',
        secondary='inscripciones',
        back_populates='alumnos'
    )


# =========================
# MAESTROS
# =========================
class Maestros(db.Model):
    __tablename__ = 'maestros'
    
    matricula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    especialidad = db.Column(db.String(50))
    email = db.Column(db.String(50))
    
    # Relación uno a muchos con cursos
    cursos = db.relationship('Cursos', back_populates='maestro')


# =========================
# CURSOS
# =========================
class Cursos(db.Model):
    __tablename__ = 'cursos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(200))
    
    # FK al maestro (1 a muchos)
    maestro_id = db.Column(
        db.Integer,
        db.ForeignKey('maestros.matricula'),
        nullable=False
    )
    
    maestro = db.relationship('Maestros', back_populates='cursos')
    
    # Relación muchos a muchos con alumnos
    alumnos = db.relationship(
        'Alumnos',
        secondary='inscripciones',
        back_populates='cursos'
    )