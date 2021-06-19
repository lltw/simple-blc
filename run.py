from flask_cors import CORS
from simple_benfords_law_checker import create_app

app = create_app()

cors = CORS(app, resources={r'/*': {'origins': 'http://localhost:8080/*'}})


if __name__ == "__main__":
    app.run()
