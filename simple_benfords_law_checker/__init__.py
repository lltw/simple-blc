import os

from flask import Flask
from mongoengine import connect


def get_db():
    db_name = 'test_mongodb'
    # host = 'localhost' #/local
    host = 'db'
    port = 27017
    username = 'root'
    password = 'pass'

    client = connect(
        'test_mongodb', host=f'mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource=admin')
    db = client['test_mongodb']

    return db


db = get_db()
current_user_files = db.current_user_files
user_submitted_data = db.user_submitted_data


# TODO: store config in config objects or config files


def create_app():
    """Initialize the core application."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_DIR=('/var/www/uploads/'),
        ALLOWED_EXTENSIONS={'tsv', 'csv', 'txt', 'tab'},
        MAX_FILENAME_LEN=200,
        ALLOWED_DELIMITERS={'comma': '\x2C', 'semicolon': '\x3B',
                            'colon': '\x3A', 'tab': '\x09', 'space': '\x20'},
        MAX_CONTENT_LENGTH=10 * 1024 * 1024,  # set maximum upload file size to 1MB
        ALLOWED_MIN_NO_RECORDS=100,
        ALLOWED_MAX_FRAC_MALFORMED_RECORDS=0.1,
    )

    # ensure the instance folder exists
    # TODO: use logger instead of printing
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as error:
        print(error)

    # ensure the upload folder exists
    try:
        os.makedirs(app.config['UPLOAD_DIR'], exist_ok=True)
    except OSError as error:
        print('Couldn\'t create an upload directory')
        print(error)

    with app.app_context():

        from . import views

        # Register Blueprints
        app.register_blueprint(views.api_bp, url_prefix="/")

        return app
