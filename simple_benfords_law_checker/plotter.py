import os
import uuid
import numpy as np
from matplotlib.figure import Figure
import matplotlib.axes._axes as axes  # code completion aid
from simple_benfords_law_checker.models import CurrentUserFile


def get_benfords_freq_dist():
    freq_dist = np.zeros(9)
    for d in range(1, 10):
        freq_dist[d-1] = np.log10(1 + (d)**(-1))
    return freq_dist


BENFORD_FREQ_DIST = get_benfords_freq_dist()


def get_first_significant_digit(number):
    return int(str(number).lstrip('0').lstrip('.')[0])


def get_emp_freq_distribution(data):

    n = len(data)
    emp_freq_dist = np.zeros(9)

    for i in range(n):
        emp_freq_dist[data[i] - 1] += 1

    emp_freq_dist /= n

    return emp_freq_dist


def get_freq_dist_plot(file_id: uuid) -> Figure:

    current_user_file = CurrentUserFile.get_by_file_id(file_id)
    data_column = current_user_file.data_column

    data = [get_first_significant_digit(float(x)) for x in data_column]

    labels = [str(i) for i in range(1, 10)]

    data_emp_freq_dist = get_emp_freq_distribution(data)

    x = np.arange(len(labels))
    width = 0.30

    fig = Figure()  # type: Figure
    ax = fig.subplots()  # type: axes.Axes

    ax.bar(x - 0.15, BENFORD_FREQ_DIST, width, label='Distribution according to Benford\'s law ')
    ax.bar(x + 0.15, data_emp_freq_dist, width, label='Distribution in data provided by a User')

    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of first significant digit')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    return fig


