from flask import render_template, flash, url_for, redirect, request
from FlaskHg import app, db, bcrypt
from FlaskHg.forms import RegistrationForm, LoginForm, UpdateAccountForm
from FlaskHg.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
	{
		'author': 'Omar Mejia',
		'title': 'Reestructurando los Recursos',
		'content': 'Para ser editado muy pronto',
		'date_posted': 'November 14, 2019'
	},
	{
		'author': 'Colaborador 2',
		'title': 'Como ser contratistas?',
		'content': 'Definir objetivos concretos para el siguiente año.',
		'date_posted': 'November 14, 2019'
	}
]

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html', title='About')

@app.route('/blog')
def blog():
	return render_template('blog.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('blog'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
		db.session.add(user)
		db.session.commit()
		flash(f'La cuenta para el usuario { form.username.data }, ha sido creada!', 'success')
		return redirect(url_for('blog'))
	return render_template('register.html', title='HG Registro', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('blog'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('blog'))
		else:
			flash('Error en el inicio de sesión.', 'danger')
	return render_template('login.html', title='NT Iniciar Sesión', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('blog'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Tu cuenta ha sido actualiada!', 'sucess')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Cuenta', image_file=image_file, form=form)