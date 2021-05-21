from flask_cors import CORS
from simple_benfords_law_checker import create_app

app = create_app()

CORS(app)  # , resources={r'/*': {'origins': '*'}})


if __name__ == "__main__":
    app.run()
