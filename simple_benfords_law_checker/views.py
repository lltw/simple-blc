import os
import uuid

from flask import flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from simple_benfords_law_checker import app

from simple_benfords_law_checker.parser import (is_upload_file_html_form_ok,
                                                parse_upload_file_html_form,
                                                is_column_in_range,
                                                save_current_user_file,
                                                parse_user_submitted_file)

from simple_benfords_law_checker.models import CurrentUserFile


@app.route('/')
def index():
    return render_template('index.html')


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

                # Parse user 'Upload File' HTML form
                column, delimiter, is_header = parse_upload_file_html_form(column, delimiter, is_header)

                if is_column_in_range(file, column, delimiter, is_header):

                    # Generate id for user submitted file. Save user submitted file to UPLOAD_DIR/file_id/
                    file_id: uuid = save_current_user_file(file, filename)

                    # Parse user submitted file
                    current_user_file = parse_user_submitted_file(file_id,
                                                                  filename,
                                                                  column,
                                                                  delimiter,
                                                                  is_header)    # type: CurrentUserFile

                    # Save current_user_file to current_user_files database
                    current_user_file.save()

                    return redirect(url_for('show_results', file_id=file_id))

            return render_template('index.html')

    return render_template('index.html')




@app.route('/<file_id>/result', methods=['GET', 'POST'])
def show_results(file_id: uuid):

    # Generate the figure
    from . import plotter
    from io import BytesIO
    import base64

    from simple_benfords_law_checker.benfords_stats import chisquare_gof_benfords_law_test

    fig = plotter.get_freq_dist_plot(file_id)

    current_user_file = CurrentUserFile.get_by_file_id(file_id)
    numbers = current_user_file.data_column

    chi_2_statistic, chi_2_p_value = chisquare_gof_benfords_law_test(numbers)

    # Save it to a temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format='png')

    # Embed the result in the html output
    freq_dist_plot = base64.b64encode(buf.getbuffer()).decode('ascii')

    return render_template('result.html',
                           freq_dist_plot=freq_dist_plot,
                           chi_2_statistic=chi_2_statistic,
                           chi_2_p_value=chi_2_p_value)


@app.route('/db-test')
def db_test():
    from . import user_submitted_data

    wild_humans = user_submitted_data.find_one({"type": "wild"})
    text = f"Wild humans are: {wild_humans}"


    return render_template('db-test.html', text=text)
