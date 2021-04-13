from simple_benfords_law_checker import app, user_submitted_data

import os
from flask import flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def is_upload_file_html_form_ok(file, filename, column, delimiter, is_header) -> bool:
    """Check if all the fields of 'Upload File' HTML form are correctly filled,
     generate error if not."""

    is_form_ok = False
    error_messages = []

    if not file:
        error_messages.append('No file selected.')
    else:
        if not allowed_file(filename):
            error_messages.append('Invalid file extension. Valid extensions are: ' +
                                  ', '.join(app.config['ALLOWED_EXTENSIONS']))

        # TODO: check if number of column is convertible to an integer
        #       greater than 1
        if not column:
            error_messages.append('No column specified.')

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


@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        if request.files:
            file = request.files['file']
            column = request.form['column']
            delimiter = request.form['delimiter']
            is_header = request.form['is_header']

            filename = secure_filename(file.filename)

            if is_upload_file_html_form_ok(file, filename, column, delimiter, is_header):

                # Generate file ID and create file dir in upload dir
                # TODO: change the user file ID generation system to something less naive
                #       and put it into more appropriate place
                from numpy import random
                file_id = str(random.randint(1, 99999))

                # Save file to UPLOAD_DIR/file_id/
                file_dir = os.path.join(app.config['UPLOAD_DIR'], file_id)
                os.makedirs(file_dir)
                file_path = os.path.join(file_dir, filename)
                file.save(file_path)

                # Parse the file
                column = int(column) - 1
                delimiter = app.config['ALLOWED_DELIMITERS'][delimiter]
                is_header = True if is_header == 'yes' else False

                from . import parser
                parser.parse_user_provided_data(file_dir, file_id, filename,
                                                column, delimiter, is_header)

                return redirect(url_for('show_results', file_id=file_id))

            return render_template('index.html')

    return render_template('index.html')


@app.route('/<file_id>/result', methods=['GET', 'POST'])
def show_results(file_id: str):

    # Generate the figure
    from . import plotter
    from io import BytesIO
    import base64

    fig = plotter.get_freq_dist_plot(file_id)

    # Save it to a temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format='png')

    # Embed the result in the html output
    freq_dist_plot = base64.b64encode(buf.getbuffer()).decode('ascii')

    return render_template('result.html', freq_dist_plot=freq_dist_plot)


@app.route('/db-test')
def db_test():

    wild_humans = user_submitted_data.find_one({"type": "wild"})
    text = f"Wild humans are: {wild_humans}"

    return render_template('db-test.html', text=text)
