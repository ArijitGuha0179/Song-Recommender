from flask import Flask, render_template, request
import pandas as pd
from model import recommend_songs
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        song_name = request.form['song_name']
        song_year = int(request.form['song_year'])
        song_list = [{'name': song_name, 'year': song_year}]
        data = pd.read_csv("./input/data.csv")
        recommended_songs = recommend_songs(song_list, data)

        # Store recommended songs in the database
        for song in recommended_songs:
            new_song = Song(name=song['name'], year=song['year'])
            db.session.add(new_song)
        db.session.commit()

        return render_template('result.html', songs=recommended_songs)
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)