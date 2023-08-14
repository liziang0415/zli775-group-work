"""Initialize Flask app."""

from flask import Flask, render_template

# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from games.domainmodel.model import Game

app = Flask(__name__)


@app.route('/')
def home():
    # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
    return render_template("gameDescription.html")


if __name__ == "__main__":
    app.run(debug=True)
