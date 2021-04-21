import csv
import os
import uuid
from typing import List
from flask import flash
from werkzeug.datastructures import FileStorage
from simple_benfords_law_checker import app
from simple_benfords_law_checker.models import CurrentUserFile


def allowed_extension(filename: str) -> bool:
    """ Check if user submitted file has and extension that is in ALLOWED_EXTENSIONS list specified in app config. """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def allowed_filename_len(filename: str) -> bool:
    """ Check if user submitted filename does not exceed MAX_FILENAME_LEN limit specified in app config. """
    return len(filename) <= app.config['MAX_FILENAME_LEN']


def is_str_an_positive_int(x: str) -> bool:
    """ Check if string is convertible to positive integer. """
    try:
        float(x)
    except ValueError:
        return False

    if float(x).is_integer() and float(x) >= 1:
        return True
    else:
        return False


def is_upload_file_html_form_ok(file: FileStorage,
                                filename: str,
                                column: str,
                                delimiter: str,
                                is_header: bool) -> bool:
    """Check if all the fields of 'Upload File' HTML form are correctly filled,
     generate errors if not."""

    is_form_ok: bool = False
    error_messages: List[str] = []

    if not file:
        error_messages.append('No file selected.')
    else:
        if not allowed_extension(filename):
            error_messages.append('Invalid file extension. Valid extensions are: ' +
                                  ', '.join(app.config['ALLOWED_EXTENSIONS']))
        if not allowed_filename_len(filename):
            error_messages.append(f"Filename is too long. Maximum filename length is {str(app.config['MAX_FILENAME_LEN'])}")

        if not column:
            error_messages.append('No column number specified.')
        elif not is_str_an_positive_int(column):
            error_messages.append('Column number should be an integer equal or greater than 1.')

        if not delimiter:
            error_messages.append('No delimiter specified.')

        if not is_header:
            error_messages.append('No header information provided.')

    if not error_messages:
        is_form_ok = True
    else:
        for em in error_messages:
            flash(em)

    return is_form_ok


def parse_upload_file_html_form(column: str,
                                delimiter: str,
                                is_header: bool) -> (int, str, bool):
    """ Parse the fields of 'Upload File' HTML form.

    Parse column, delimiter and is_header:
    - convert column to int and change convention from 1-based to 0-based
    - get delimiter from dictionary
    - convert is header to bool
     """
    column: int = int(column) - 1
    delimiter: str = app.config['ALLOWED_DELIMITERS'][delimiter]
    is_header: bool = True if is_header == 'yes' else False

    return column, delimiter, is_header


def save_current_user_file(file: FileStorage,
                           filename: str) -> uuid:
    """ Generate file_id and save user submitted file to UPLOAD_DIR/file_id directory. """

    file_id = uuid.uuid4()
    # TODO: ensure proper file_dir creation
    file_dir = os.path.join(app.config['UPLOAD_DIR'], str(file_id))
    os.makedirs(file_dir)
    file_path = os.path.join(file_dir, filename)
    file.save(file_path)

    return file_id


def is_column_in_range(file: FileStorage, column: int, delimiter: str, is_header: bool) -> bool:
    """ Check if number of column specified by a user is not exceeding the number of columns in the header or
    in the first line of the file. Generate errors if it does."""

    column_in_range: bool = False
    first_line_len: int = len(file.stream.readline().decode().strip().split(delimiter))
    file.stream.seek(0)

    if column < first_line_len:
        column_in_range = True
    else:
        if is_header:
            flash(f'Provided column number exceeds the number of columns defined in the header: '
                  f'{str(first_line_len)}.')
        else:
            flash(f'Provided column number exceeds the number of columns found in the first row of file:'
                  f' {str(first_line_len)}.')

    return column_in_range


def parse_user_submitted_file(file_id: uuid,
                              filename: str,
                              column: int,
                              delimiter: str,
                              is_header: bool) -> CurrentUserFile:
    """ Parse user submitted file.

    """

    # TODO: Write automated tests testing for at least the following cases:
    #       (1) a value in a row can't be converted to float
    #       (2) rows have inconsistent delimiters
    #       (3) there are spaces inside strings of space delimited files

    file_dir = os.path.join(app.config['UPLOAD_DIR'], str(file_id))
    file_path = os.path.join(file_dir, filename)

    data_column: List[float] = []   # a list of values from the column selected by a user
    ncol_err_rows_nums: List[int] = []   # row numbers of rows in which number of columns deviates from the number
    # of columns in the header / first row
    val_err_rows_nums: List[int] = []    # row numbers of rows with values in data column that can't be converted
    # to float

    with open(file_path, 'r') as user_file:
        reader = csv.reader(user_file, delimiter=delimiter)

        # Get a number of columns from the first row
        first_row = next(reader)
        ncols = len(first_row)

        # If header is present - skip it, else - parse the first row
        if is_header:
            pass
        else:
            # Get value from data column. If the value cannot be converted to float, save the number of the row.
            try:
                number = float(first_row[column])
                data_column.append(number)
            except ValueError:
                val_err_rows_nums.append(reader.line_num)

        # Get the data column from the remaining of file
        for row in reader:
            # Check if number of columns is the same as in the header / first row.
            # If it's not, save the number of the row.
            if len(row) != ncols:
                ncol_err_rows_nums.append(reader.line_num)
            else:
                # Get value from data column. If the value cannot be converted to float, save the number of the row.
                try:
                    number = float(row[column])
                    data_column.append(number)
                except ValueError:
                    val_err_rows_nums.append(reader.line_num)

        # Calculate number of total rows and rows with errors
        no_lines: int = reader.line_num
        no_ncol_err: int = len(ncol_err_rows_nums)
        no_val_err: int = len(val_err_rows_nums)

        # Check if there were any errors
        are_errors_present = False
        if no_ncol_err + no_val_err > 0:
            are_errors_present = True

        # Create a CurrentUserFile object
        current_user_file = CurrentUserFile(file_id=file_id,
                                            filename=filename,
                                            file_path=file_path,
                                            data_column=data_column,
                                            are_errors_present=are_errors_present,
                                            no_lines=no_lines,
                                            no_ncol_err=no_ncol_err,
                                            no_val_err=no_val_err,
                                            ncol_err_rows_nums=ncol_err_rows_nums,
                                            val_err_rows_nums=val_err_rows_nums,
                                            )

        return current_user_file


def save_subset_of_rows_to_file(file_path, row_nums, output_file_path):

    row_nums_index = 0

    with open(file_path, 'r') as user_file, \
            open(output_file_path, 'a') as output_file:
        for i, line in enumerate(user_file):
            try:
                if i == row_nums[row_nums_index] - 1:
                    output_file.write(line)
                    row_nums_index += 1
                i += 1
            except IndexError:
                break
