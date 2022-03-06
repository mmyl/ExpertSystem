from flask import Flask, render_template, url_for, request, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    impact = db.Column(db.Integer, nullable=False)
    likelihood = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    
def __repr__(self):
    return '<Row %r>' % self.id

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        new_question = request.form['question']
        new_impact = request.form['impact']
        new_likelihood = request.form['likelihood']
        update = Question(question=new_question, impact=new_impact, likelihood=new_likelihood )

        try:
            db.session.add(update)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your row'

    else:
        rows = Question.query.order_by(Question.date_created).all()
        return render_template('index.html', rows=rows)

@app.route('/survey', methods=['POST', 'GET'])
def survey():
    if request.method == 'POST':
        sum = 0
        for key, value in request.form.items():
            # print(f"{key} : {value}")
            if value == "yes" :
                row = Question.query.get_or_404(key)
                sum = sum + row.likelihood
        print(sum)
        return redirect('/survey')
    else:
        rows = Question.query.order_by(Question.date_created).all()
        return render_template('survey.html', rows=rows)
        
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    row_to_delete = Question.query.get_or_404(id)

    try:
        db.session.delete(row_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that row'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    row = Question.query.get_or_404(id)
    
    if request.method == 'POST':
        row.question = request.form['question']
        row.impact = request.form['impact']
        row.likelihood = request.form['likelihood']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your row'

    else:
        return render_template('update.html', row=row)


if __name__ == "__main__":
    app.run(debug=True)
