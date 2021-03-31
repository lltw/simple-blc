import os
from flask import Flask

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    UPLOAD_DIR=os.path.join(app.instance_path, 'upload-dir'),
    USER_COL='user_col',
    NCOL_ERR_FILENAME='ncol_err.txt',
    VAL_ERR_FILENAME='val_err.txt',
    ALLOWED_EXTENSIONS={'tsv', 'csv', 'txt', 'tab'},
    ALLOWED_DELIMITERS={'comma': '\x2C', 'semicolon': '\x3B', 'colon': '\x3A',  'tab': '\x09',  'space': '\x20'},
    MAX_CONTENT_LENGTH=10 * 1024 * 1024,  # set maximum upload file size to 10MB
    ALLOWED_MIN_NO_RECORDS=100,
    ALLOWED_MAX_FRAC_MALFORMED_RECORDS=0.1,
)

# ensure the instance folder exists
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

# import views
from simple_benfords_law_checker import views

