import os
from flask import Flask
from pymongo import MongoClient

# TODO: refactor - use app factory pattern
# TODO: store config in config objects or config files

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    UPLOAD_DIR=('/var/www/uploads/'),
    USER_COL='user_col',
    NCOL_ERR_FILENAME='ncol_err.txt',
    VAL_ERR_FILENAME='val_err.txt',
    ALLOWED_EXTENSIONS={'tsv', 'csv', 'txt', 'tab'},
    ALLOWED_DELIMITERS={'comma': '\x2C', 'semicolon': '\x3B', 'colon': '\x3A',  'tab': '\x09',  'space': '\x20'},
    MAX_CONTENT_LENGTH=10 * 1024 * 1024, # set maximum upload file size to 1MB
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


# initialize the database
def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                         authSource="admin")

    db = client.test_mongodb
    return db


db = get_db()
user_submitted_data = db.user_submitted_data

# import views
from simple_benfords_law_checker import views

