import csv
import os
from simple_benfords_law_checker import app


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


def parse_user_provided_data(file_dir: str, file_id: str, filename: str, column: int, delimiter: str, is_header: bool):
    """ Parse user uploaded file.

    Parse user uploaded file and save the following files under
    UPLOAD_DIR/FILE_ID directory:
      - USER_COL (comma-delimited string of floats)
      - NCOL_ERR_FILENAME (file containing rows with number of
        columns deviating from the number of columns in header / first row
      - VAL_ERR_FILENAME (file containing rows with values in
        user-selected column couldn't be converted to float)

    """

    # TODO: Write automated tests testing for at least the following cases:
    #       (1) a value in a row can't be converted to float
    #       (2) rows have inconsistent delimiters
    #       (3) there are spaces inside strings of space delimited files

    # TODO: User specified column is out of range

    file_path = os.path.join(file_dir, filename)
    user_col_path = os.path.join(file_dir, app.config['USER_COL'])
    val_err_path = os.path.join(file_dir, app.config['VAL_ERR_FILENAME'])
    ncol_err_path = os.path.join(file_dir, app.config['NCOL_ERR_FILENAME'])

    user_column = []
    ncol_err_row_nums = []
    val_err_row_nums = []

    # Read user uploaded file
    with open(file_path, 'r') as user_file:
        reader = csv.reader(user_file, delimiter=delimiter)

        # Get number of columns from the first row
        first_row = next(reader)
        ncol = len(first_row)

        # If header is present - skip it, else - parse the first row
        if is_header:
            pass
        else:
            # Get value from user specified column. If the value cannot be converted
            # to float, save the number of the row.
            try:
                number = float(first_row[column])
                user_column.append(number)
            except ValueError as err:
                print(reader.line_num)
                val_err_row_nums.append(reader.line_num)

        # Get the data column from the remaining of file
        for row in reader:
            # Check if number of columns is the same as in the header / first row.
            # If it's not, save the number of the row.
            if len(row) != ncol:
                ncol_err_row_nums.append(reader.line_num)
            else:
                # Get value from user specified column. If the value cannot be converted
                # to float, save the number of the row.
                try:
                    number = float(row[column])
                    user_column.append(number)
                except ValueError as err:
                    val_err_row_nums.append(reader.line_num)


        no_lines = reader.line_num

        # Save results to files
        with open(user_col_path, 'w') as user_col_file:
            user_col_file.write(','.join([str(x) for x in user_column]))

        save_subset_of_rows_to_file(file_path, ncol_err_row_nums, ncol_err_path)
        save_subset_of_rows_to_file(file_path, val_err_row_nums, val_err_path)
