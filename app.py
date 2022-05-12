import requests
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)



class NameForm(FlaskForm):
    name = StringField('Introduce here your Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/Register/<typeUser>', methods=['GET', 'POST'])
def register(typeUser):
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('status'))
    return render_template('register.html', form=form, name=session.get('name'), typeUser=typeUser)


@app.route('/Status', methods=['GET'])
def status():
    return render_template('status.html', name=session.get('name'))


@app.route('/')
def index():
    return render_template('index.html')

    

@app.route('/Episodes/Titans')
def episodes():
    URL = "https://en.wikipedia.org/wiki/Titans_(2018_TV_series)"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup.find_all("tr", class_="vevent")
    x=0
    episodes=[]
    for row in rows:
        x+=1
        episodes.append(str(x)+ " " + (row.find("td", class_="summary")).text.strip())
    return("<br>".join(episodes))