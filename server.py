import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime, timedelta


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
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
    other_clubs = [other_club for other_club in clubs if not other_club['email'] == request.form['email']]
    return render_template('welcome.html',club=club,competitions=competitions,other_clubs=other_clubs)


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
            return render_template('welcome.html', club=foundClub, competitions=competitions)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    other_clubs = [other_club for other_club in clubs if not other_club['email'] == club['email']]
    placesRequired = int(request.form['places'])
    if int(competition['numberOfPlaces']) >= placesRequired and placesRequired<=12:
        if int(club['points']) < placesRequired:
            flash("you don't have enough points!")
            return render_template('welcome.html', club=club, competitions=competitions, other_clubs=other_clubs)
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points'])-placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions, other_clubs=other_clubs)
    else:
        flash('You may not reserve more than 12 places per competition!')
        return render_template('welcome.html', club=club, competitions=competitions, other_clubs=other_clubs)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))