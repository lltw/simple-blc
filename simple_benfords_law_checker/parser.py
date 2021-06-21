import csv
import os
import uuid
from typing import List

from werkzeug.datastructures import FileStorage

from simple_benfords_law_checker.models import CurrentUserFile
from flask import current_app as app


def save_current_user_file(file: FileStorage,
                           filename: str) -> uuid:
    """
    Generate file_id and save user submitted file to UPLOAD_DIR/file_id directory.
    """

    file_id = uuid.uuid4()
    # TODO: ensure proper file_dir creation
    file_dir = os.path.join(app.config['UPLOAD_DIR'], str(file_id))
    os.makedirs(file_dir)
    file_path = os.path.join(file_dir, filename)
    file.save(file_path)

    return file_id


def parse_user_submitted_file(file_id: uuid,
                              filename: str,
                              column: int,
                              delimiter: str,
                              is_header: bool) -> CurrentUserFile:
    """
    Parse user submitted file.
    TODO: write this description
    """

    # TODO: Write automated tests testing for at least the following cases:
    #       (1) a value in a row can't be converted to float
    #       (2) rows have inconsistent delimiters
    #       (3) there are spaces inside strings of space delimited files

    file_dir = os.path.join(app.config['UPLOAD_DIR'], str(file_id))
    file_path = os.path.join(file_dir, filename)

    # a list of values from the column selected by a user
    data_column: List[float] = []
    # row numbers of rows in which number of columns deviates from the number
    ncol_err_rows_nums: List[int] = []
    # of columns in the header / first row
    # row numbers of rows with values in data column that can't be converted
    val_err_rows_nums: List[int] = []
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
