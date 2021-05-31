import os
import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime, timedelta


def loadClubs():
    directory = os.path.dirname(__file__)
    path_to_file = os.path.join(directory, 'clubs.json')
    with open(path_to_file) as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    directory = os.path.dirname(__file__)
    path_to_file = os.path.join(directory,'competitions.json')
    with open(path_to_file) as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)

@app.route('/clubs',methods=['GET'])
def showClubs():
    return render_template('clubs.html',clubs=clubs)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    date_2_days_ago = datetime.now() - timedelta(days=2)
    if foundClub and foundCompetition:
        if datetime.strptime(foundCompetition['date'],'%Y-%m-%d %H:%M:%S')>date_2_days_ago:
            return render_template('booking.html',club=foundClub,competition=foundCompetition)
        else:
            flash("This competition is passed you can't book places anymore")
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if int(competition['numberOfPlaces']) >= placesRequired and placesRequired<=12 and placesRequired>=0:
        if int(club['points']) < placesRequired:
            flash("you don't have enough points!")
            return render_template('welcome.html', club=club, competitions=competitions)
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points'])-placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash('You may not reserve more than 12 places per competition!')
        return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))