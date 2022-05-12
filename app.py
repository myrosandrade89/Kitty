import requests
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from bs4 import BeautifulSoup
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)



class NameForm(FlaskForm):
    name = StringField('Introduce here your Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


def getNamesDescriptionBreeds(breeds): 
    finalNames = []

    for breed in breeds: 
        finalNames.append(breed["name"])

    return finalNames

class KittyForm(FlaskForm): 
    breeds = requests.get("https://api.thecatapi.com/v1/breeds").json()
    breedNames = getNamesDescriptionBreeds(breeds)

    nameKitty = StringField('Introduce el nombre de tu michi/gatito: ', validators=[DataRequired(), Length(max=64)])
    nameOfOwner = StringField('Introduce tu nombre: ', validators=[DataRequired(), Length(max=64)])
    breed = SelectField('raza', choices=breedNames)
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/michiGordo')
def status():
    URL = "https://en.wikipedia.org/wiki/Meow_(cat)"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    information = soup.find("table", class_="infobox biography biota")

    name=information.find("caption", class_="infobox-title").text.strip()
    image=information.find("img")
    img=image["src"]


    dataSets=information.find_all("td")
    species=dataSets[1].text.strip()
    sex=dataSets[2].text.strip()
    description=dataSets[6].text.strip()
    return render_template('datoCurioso.html', name=name, image=img, description=description, sex=sex, species=species)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = KittyForm()
    if(request.method == "GET"):
        return render_template('index.html', form = form)
    else: 
        if form.validate_on_submit(): 
            kittyName = form.nameKitty.data
            useranme = form.nameOfOwner.data
            breed = form.breed.data
            
            kittyData = requests.get(f'https://api.thecatapi.com/v1/images/search?breed_name={breed}').json()[0]["url"]
            
            return render_template('kitty.html', nameKitty=kittyName, nameOwner = useranme, url= kittyData)
