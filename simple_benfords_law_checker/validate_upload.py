
from typing import Tuple

from flask import current_app as app

from flask import abort, jsonify, make_response
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import RequestEntityTooLarge


@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def app_handle_413(e):
    error_message = f"Submitted file is too large. Maximum accepted size is {str(app.config['MAX_CONTENT_LENGTH']/(1024 * 1024))} MB."
    return jsonify({'message': error_message}), 413


def is_upload_request_complete(request) -> bool:
    """Checks if all required fields are present in the upload request. If not, aborts with HTTP response status code 400 and custom message, otherwise returns True."""
    if 'file' not in request.files:
        abort(make_response(jsonify({'message': 'No file was sent.'}), 400))

    lacking_fields = []

    if 'delimiter' not in request.form:
        lacking_fields.append('delimiter')
    if 'isHeader' not in request.form:
        lacking_fields.append('isHeader')
    if 'columnNumber' not in request.form:
        lacking_fields.append('columnNumber')

    if len(lacking_fields) > 0:
        error_message = "Not all reqired fields were present in the request. Lacking fields: " + \
            ', '.join(lacking_fields)
        abort(make_response(jsonify({'message': error_message}), 400))

    return True


def validate_filename(filename: str) -> None:
    """Validates uploaded filename parameters. If invalid, aborts with HTTP response status code 400 and custom message, otherwise returns None."""
    if len(filename) > app.config['MAX_FILENAME_LEN']:
        error_message = f"Name of submitted file is too large. Maximum accepted length is {str(app.config['MAX_FILENAME_LEN'])}."
        abort(make_response(jsonify({'message': error_message}), 400))

    if not '.' in filename or not filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
        error_message = f"Name of submitted file is too large. Maximum accepted length is {str(app.config['MAX_FILENAME_LEN'])}."
        abort(make_response(jsonify({'message': error_message}), 400))


def validate_and_parse_delimiter(delimiter: str) -> str:
    """Tries to parse the delimiter. If fails, aborts with HTTP response status code 400 and custom message."""
    try:
        delimiter: str = app.config['ALLOWED_DELIMITERS'][delimiter]
    except KeyError:
        error_message = f"Delimiter is not allowed. Allowed delimiters are {str(app.config['ALLOWED_DELIMITERS'])}."
        abort(make_response(jsonify({'message': error_message}), 400))
    return delimiter


def validate_and_parse_is_header(is_header: str) -> bool:
    """Tries to parse the delimiter. If fails, aborts with HTTP response status code 400 and custom message."""
    if is_header == 'true':
        return True
    elif is_header == 'false':
        return False
    else:
        error_message = f"'IsHeader' containes invalid value. Allowed values are 'true' or 'false'."
        abort(make_response(jsonify({'message': error_message}), 400))


def is_str_an_positive_int(x: str) -> bool:
    """Checks if string is convertible to positive integer."""
    try:
        float(x)
    except ValueError:
        return False

    if float(x).is_integer() and float(x) >= 1:
        return True
    else:
        return False


def validate_and_parse_column(column: str) -> int:
    """Tries to parse column number is positive integer. If fails, aborts with HTTP response status code 400 and custom message."""
    if is_str_an_positive_int(column):
        return int(column) - 1
    else:
        error_message = f"'columnNumber' containes invalid value. Column number should be string convertible to an integer equal or greater than 1."
        abort(make_response(jsonify({'message': error_message}), 400))


def validate_and_parse_file_metadata(column: str,
                                     delimiter: str,
                                     is_header: bool) -> Tuple[int, str, bool]:
    """Validates and tries to parse the fields of upload request. If invalid, aborts with HTTP response status code 400 and custom message, otherwise returns Tuple[int, str, bool].


    Parse column, delimiter and is_header:
    - convert column to int and change the order from 1-based to 0-based
    - get delimiter from dictionary
    - convert is_header to bool
     """

    is_header = validate_and_parse_is_header(is_header)
    delimiter = validate_and_parse_delimiter(delimiter)
    column = validate_and_parse_column(column)

    return column, delimiter, is_header


def is_column_in_range(file: FileStorage, column: int, delimiter: str, is_header: bool) -> bool:
    """Check if number of column specified by a user is not exceeding the number of columns in the header or in the first line of the file. Generate errors if it does."""

    column_in_range: bool = False
    first_line_len: int = len(
        file.stream.readline().decode().strip().split(delimiter))
    file.stream.seek(0)

    if column < first_line_len:
        column_in_range = True
    else:
        if is_header:
            error_message = f'Provided column number exceeds the number of columns defined in the header: {str(first_line_len)}.'
            abort(make_response(jsonify({'message': error_message}), 400))
        else:
            error_message = f'Provided column number exceeds the number of columns found in the first row of file: {str(first_line_len)}.'
            abort(make_response(jsonify({'message': error_message}), 400))

    return column_in_range
