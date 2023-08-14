from games.adapters.datareader import GameFileCSVReader
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("layout.html")


@app.route('/games')
def game():
    page = request.args.get('page', 1, type=int)  # Default to page 1 if not provided
    per_page = 18  # Number of games per page
    offset = (page - 1) * per_page

    reader = GameFileCSVReader("games/adapters/datareader/games.csv")
    reader.read_csv_file()
    nmsl = reader.dataset_of_games
    nmsl.sort(key=lambda x: x.title)

    games_to_display = nmsl[offset:offset + per_page]

    return render_template("games.html", games=games_to_display, page=page)
