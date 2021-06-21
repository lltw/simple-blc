import re
import sys
import uuid

from flask import render_template, jsonify, send_file, request, Blueprint, abort

from werkzeug.utils import secure_filename
from flask import current_app as app

from simple_benfords_law_checker.validate_upload import (is_upload_request_complete,
                                                         validate_filename,
                                                         validate_and_parse_file_metadata,
                                                         is_column_in_range)

from simple_benfords_law_checker.parser import (save_current_user_file,
                                                parse_user_submitted_file)

from simple_benfords_law_checker.models import CurrentUserFile

from simple_benfords_law_checker.benfords_stats import chisquare_gof_benfords_law_test


# Blueprint Configuration
api_bp = Blueprint(
    'api_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='static',
)


@app.route('/upload-file', methods=['POST'])
def upload_file():

    # Check, if request contains 'file', 'delimiter', 'isHeader' and 'columnNumber' data
    if is_upload_request_complete(request):

        file = request.files['file']
        delimiter = request.form['delimiter']
        is_header = request.form['isHeader']
        column = request.form['columnNumber']

        # Sanitize and validate filename
        filename = secure_filename(file.filename)
        validate_filename(filename)

        # Validate and try to parse metadata.
        (column, delimiter, is_header) = validate_and_parse_file_metadata(
            column, delimiter, is_header)

        # Chech if column is in range
        is_column_in_range(file, column, delimiter, is_header)

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

        response_object = {'status': 'success', 'fileID': str(file_id)}

        return jsonify(response_object)
    else:
        abort(500)


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


@app.route('/chi-squared-results', methods=['GET'])
def chi_squared_results():

    file_id = request.args.get('fileID')

    current_user_file = CurrentUserFile.get_by_file_id(file_id)
    numbers = current_user_file.data_column

    chi_2_statistic, chi_2_p_value = chisquare_gof_benfords_law_test(numbers)

    response_object = {'status': 'succes'}
    response_object['chiSquaredStatistic'] = chi_2_statistic
    response_object['chiSquaredPvalue'] = chi_2_p_value

    return jsonify(response_object)


@app.route('/plot', methods=['GET'])
def plot():

    file_id = request.args.get('fileID')

    from . import plotter
    import os

    fig = plotter.get_freq_dist_plot(file_id)

    fig_path = os.path.join(app.config['UPLOAD_DIR'], str(file_id), 'plot.png')
    fig.savefig(fig_path)

    return send_file(fig_path, mimetype='image/jpg')


@app.route('/db-test')
def db_test():
    from . import user_submitted_data

    wild_humans = user_submitted_data.find_one({"type": "wild"})
    text = f"Wild humans are: {wild_humans}"

    return render_template('db-test.html', text=text)


@app.route('/test-results-stats', methods=['GET'])
def test_results_stats():

    chi_2_statistic, chi_2_p_value = 5.941393249642216, 0.6537967552115286

    response_object = {'status': 'succes'}
    response_object['chiSquaredStatistic'] = chi_2_statistic
    response_object['chiSquaredPvalue'] = chi_2_p_value
    return jsonify(response_object)


@app.route('/test-results-plot', methods=['GET'])
def test_results_plot():

    filename = 'static/img/test-plot.png'
    return send_file(filename, mimetype='image/jpg')
