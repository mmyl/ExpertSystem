from unicodedata import category
from flask import Flask, render_template, url_for, request, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import pandas as pd
import plotly
import plotly.express as px

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///master.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.String(10), nullable=False)
    question = db.Column(db.String(200), nullable=False)
    impact = db.Column(db.Integer, nullable=False)
    likelihood = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(200), nullable=False)

class Facts(db.Model):
    fact_id = db.Column(db.Integer, primary_key=True)
    facts = db.Column(db.String(25), nullable=False)
    risk_description = db.Column(db.String(300), nullable=False)
    
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
    categories = Categories.query.all()
    return render_template('login.html', form=form, categories=categories)

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
        
        # Adding new category
        if "category_name" in request.form:
            new_category = request.form['category_name']
            new_description = request.form['description']
            update = Categories(category=new_category, description=new_description)
        
        # Adding new fact
        if "facts" in request.form:
            # Removing spaces
            new_fact = request.form['facts'].replace(" ", "")
            print(new_fact)
            delim = ","
            # Sorting facts
            new_fact_sorted = delim.join(sorted(new_fact.split(delim)))
            print(new_fact_sorted)
            new_risk_description = request.form['risk_description']
            update = Facts(facts=new_fact_sorted, risk_description=new_risk_description)
            
        # Adding new question
        if "question" in request.form:
            new_question = request.form['question']
            new_impact = request.form['impact']
            new_likelihood = request.form['likelihood']
            new_category = request.form['category']
            # Get max id
            max_id = db.session.query(Question.id).order_by(Question.id.desc()).first()
            if max_id == None:
                max_id = [0]
            new_question_id = new_category[0:4] + str(max_id[0])
            print(new_question_id)
            update = Question(question=new_question, impact=new_impact, likelihood=new_likelihood, category=new_category, question_id=new_question_id)
        try:
            db.session.add(update)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your row'
    
    else:
        rows = Question.query.order_by(Question.date_created).all()
        categories = Categories.query.all()
        facts = Facts.query.all()
        return render_template('index.html', rows=rows, categories=categories, facts=facts)

@app.route('/survey', methods=['POST', 'GET'])
def survey():
    if request.method == 'POST':
        sum = 0
        total = 0
        answers = []
        for key, value in request.form.items():
            if value == "yes" :
                row = Question.query.get_or_404(key)
                sum = sum + ( row.likelihood * row.impact )
                answers.append(row.question_id) 
            row = Question.query.get_or_404(key)
            total = total + ( row.likelihood * row.impact )
        print(answers)
        
        # Define powerset function    
        def powerset(s):
            x = len(s)
            masks = [1 << i for i in range(x)]
            for i in range(1 << x):
                yield [ss for mask, ss in zip(masks, s) if i & mask]
        
        # Makes all possible combinations
        answers = list(powerset(answers))
        # Join list items to strings and remove empty list items
        answers = [",".join(i) for i in answers if i]
        print(answers)
        matched_risk = Facts.query.filter(Facts.facts=='BDAR11,BDAR12,BDAR13')
        results = matched_risk.all()
        print(type(matched_risk))
        print (matched_risk.all())
        print(matched_risk.all()[0])
        print(type(matched_risk.all()[0]))
        print(dir(matched_risk.all()[0]))
        print(results[0].fact_id)
        print(results[0].facts)
        print(results[0].risk_description)
        # for each in answers:
            # matched_risk = Facts.query.get_or_404(each)
          
        return redirect(url_for('.results', sum=sum, total=total, answers = matched_risk))
    else:
        selected_category = request.args.get('category')
        rows = Question.query.filter(Question.category==selected_category)
        categories = Categories.query.all()
        return render_template('survey.html', rows=rows, categories=categories)

@app.route('/results/<sum>', methods=['POST', 'GET'])
def results(sum):
        # https://plotly.com/python/pie-charts/
        # https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946
        
        category_total = request.args.get('total')
        answers = request.args.get('answers')
        labels = ["Rizikos balai", "Surinkta"]

        # Create subplots: use 'domain' type for Pie subplot
        fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])
        fig.add_trace(go.Pie(labels=labels, values=[int(category_total)-int(sum), sum], name="Slaptažodžiai"), 1, 1)

        # Use `hole` to create a donut-like pie chart
        fig.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig.update_traces(marker=dict(colors=['red', 'green']))

        fig.update_layout(
            title_text="Rizikos vertinimo atvaizdavimas",
            # Add annotations in the center of the donut pies.
            annotations=[dict(text= sum + "/" + category_total, x=0.5, y=0.5, font_size=20, showarrow=False)])
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        categories = Categories.query.all()
        return render_template('results.html', sum=sum, graphJSON=graphJSON, categories=categories, answers=answers)
        
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
        categories = Categories.query.all()
        return render_template('update.html', row=row, categories=categories)


if __name__ == "__main__":
    app.run(debug=True)
