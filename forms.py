from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    enviar = SubmitField('Ingresar')


class SaludarForm(FlaskForm):
    usuario = StringField('Nombre: ', validators=[Required()])
    enviar = SubmitField('Saludar')


class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()])
    enviar = SubmitField('Registrarse')


class ConsultaxPais(FlaskForm):
    pais = StringField('País:', validators=[Required()])
    enviar = SubmitField('Filtrar')

class ConsultaxEdad(FlaskForm):
    edad_min = IntegerField('Edad Minima:', validators=[Required('Ingresar caracteres numéricos')])
    edad_max = IntegerField('Edad Maxima:', validators=[Required('Ingresar caracteres numéricos')])
    enviar = SubmitField('Filtrar')

class ConsultaxFecha(FlaskForm):
    fecha = StringField('Fecha:', validators=[Required()], render_kw={"placeholder": "AAAA-MM-DD"})
    enviar = SubmitField('Filtrar')    

class AgregarNuevoCliente(FlaskForm):
	nombre = StringField('Nombre', validators=[Required()])
	edad = StringField('Edad', validators=[Required()])
	direccion = StringField('Dirección', validators=[Required()])
	pais = StringField('País', validators=[Required()])
	dni = StringField('Documento', validators=[Required()])
	fecha_alta = StringField('Fecha Alta', validators=[Required()], render_kw={"placeholder": "AAAA-MM-DD"})
	mail = StringField('Correo Electrónico', validators=[Required()])
	trabajo = StringField('Trabajo', validators=[Required()])
	enviar = SubmitField('Agregar')


class AgregarNuevoProducto(FlaskForm):
    descripcion = StringField('Descripcion', validators=[Required()])
    codigo = StringField('Codigo', validators=[Required()])
    precio = StringField('Precio', validators=[Required()])
    stock = StringField('Stock', validators=[Required()])
    enviar = SubmitField('Agregar')