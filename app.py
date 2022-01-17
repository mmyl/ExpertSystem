from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    impact = db.Column(db.Integer, nullable=False)
    likelihood = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Row %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_question = request.form['question']
        new_impact = request.form['impact']
        new_likelihood = request.form['likelihood']
        update = Todo(question=new_question, impact=new_impact, likelihood=new_likelihood )

        try:
            db.session.add(update)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your row'

    else:
        rows = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', rows=rows)


@app.route('/delete/<int:id>')
def delete(id):
    row_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(row_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that row'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    row = Todo.query.get_or_404(id)

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
