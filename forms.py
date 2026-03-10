from wtforms import Form, SelectField
from flask_wtf import FlaskForm
 
from wtforms import StringField,IntegerField
from wtforms import EmailField
from wtforms import validators

class UserForm2(Form):
    id=IntegerField('id',
                    [validators.number_range(min=1, max=20, message='Valor no validos')])
    nombre=StringField('nombre',[
        validators.DataRequired(message='El nombre es requerido'),
        validators.length(min=4, max=20, message='Requiere nombre valido')
    ])
    apellidos=StringField('apellidos', [
        validators.DataRequired(message='El apellido es requerido')
    ])
    email=EmailField('correo',[
        validators.DataRequired(message='El correo es requerido'),
        validators.Email(message='Ingrese correo valido')
    ])
    telefono=StringField('telefono', [
        validators.DataRequired(message='El apellido es requerido')
    ])

class UserForm(Form):
    matricula=IntegerField('matricula',
                    [validators.number_range(min=1, max=20, message='Valor no validos')])
    nombre=StringField('nombre',[
        validators.DataRequired(message='El nombre es requerido'),
        validators.length(min=4, max=20, message='Requiere nombre valido')
    ])
    apellidos=StringField('apellidos', [
        validators.DataRequired(message='El apellido es requerido')
    ])
    especialidad=StringField('especialidad', [
        validators.DataRequired(message='El apellido es requerido')
    ])
    email=EmailField('correo',[
        validators.DataRequired(message='El correo es requerido'),
        validators.Email(message='Ingrese correo valido')
    ])

class UserFormC(Form):
    id=IntegerField('id',
                    [validators.number_range(min=1, max=20, message='Valor no validos')])
    nombre=StringField('nombre',[
        validators.DataRequired(message='El nombre es requerido'),
        validators.length(min=4, max=20, message='Requiere nombre valido')
    ])
    descripcion=StringField('descripcion', [
        validators.DataRequired(message='La descripcion es requerida')
    ])
    
    maestro_id = SelectField('maestro', coerce=int)
