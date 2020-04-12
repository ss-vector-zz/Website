from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from FlaskHg.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Nombre de Usuario',
				validators=[DataRequired(), Length(min=4, max=20)])
	email = StringField('Correo',
				validators=[DataRequired(), Email()])
	password = PasswordField('Clave', validators=[DataRequired()])
	confirm_password = PasswordField('Confirmar Clave', 
				validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Registrarse')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('El usuario ya existe.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('El e-mail ya existe.')

class LoginForm(FlaskForm):
	email = StringField('Correo',
				validators=[DataRequired(), Email()])
	password = PasswordField('Clave', validators=[DataRequired()])
	remember =BooleanField('Remember me')
	submit = SubmitField('Iniciar Sesión')

class UpdateAccountForm(FlaskForm):
	username = StringField('Nombre de Usuario',
				validators=[DataRequired(), Length(min=4, max=20)])
	email = StringField('Correo',
				validators=[DataRequired(), Email()])
	picture = FileField('Actualizar foto de perfil!', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Actualizar')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('El usuario ya existe.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('El e-mail ya existe.')
