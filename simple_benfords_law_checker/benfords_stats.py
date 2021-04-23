import numpy as np
import numpy.typing as npt
from scipy.stats import chisquare


def get_benfords_prob_dist() -> np.ndarray:
    """Calculates probability distribution of first significant digits according to Benford's Law, returns it as a np.ndarray."""

    prob_dist = np.zeros(9)
    for digit in range(1, 10):
        prob_dist[digit - 1] = np.log10(1 + digit ** (-1))
    return prob_dist


BENFORDS_PROB_DIST: npt.ArrayLike = get_benfords_prob_dist()


def get_benfords_freq_dist(sample_size: int, benfords_prob_dist: npt.ArrayLike = BENFORDS_PROB_DIST) -> np.ndarray:
    """Given a sample size, simulates a frequency distribution of first significant digits corresponding to Benford's Law, returns it as a np.ndarray."""

    freq = sample_size * benfords_prob_dist
    return freq


def get_fsd(number: float) -> int:
    """Gets a first significant digit of a float number, returns it as an int."""

    return int(str(number).lstrip('0').lstrip('.')[0])


def get_observed_fsd_frequencies(numbers: npt.ArrayLike) -> np.ndarray:
    """Calculates frequencies of first significant digits in a provided array of numbers.

    Parameters
    ----------
    numbers: npt.ArrayLike
        npt.ArrayLike object populated with ints or floats

    Returns
    -------
    np.ndarray
        an np.array of frequencies of first significant digits in a provided array of numbers
    """

    digits = [get_fsd(number) for number in numbers]
    observed_fsd_frequencies = np.zeros(9)

    for i in range(len(digits)):
        observed_fsd_frequencies[digits[i] - 1] += 1

    return observed_fsd_frequencies


def chisquare_gof_benfords_law_test(numbers: npt.ArrayLike) -> (float, float):
    """Performs Chi-squared Goodness of Fit test with Null Hypothesis: numbers follows the Benford's Distribution.

    Performs Chi-squared Goodness of Fit test to check if frequencies of first significant digits of provided data
    follow Bendford's Law. Test used: scipy.stats.chisquare.

    Parameters
    ----------
    numbers: npt.ArrayLike
        npt.ArrayLike object populated with ints or float
    Returns
    -------
    (float, float)
        Chi-square statistic and p-value for Chi-square Goodness of Fit test
    """

    observed_freq = get_observed_fsd_frequencies(numbers)
    expected_freq = get_benfords_freq_dist(len(numbers))

    chi_2_statistic, chi_2_p_value = chisquare(observed_freq, expected_freq)

    return chi_2_statistic, chi_2_p_value


def get_orders_of_magnitude(numbers: npt.ArrayLike) -> (int, int):
    """Calculates orders of magnitude of the smallest and the largest number in a provided list.

    Order of magnitude is defined as log10 of a number, truncated to an integer.

    Parameters
    ----------
    numbers: npt.ArrayLike
        a npt.ArrayLike object populated with ints or floats

    Returns
    -------
    (int, int)
        orders of magnitude of the smallest and largest number from a provided array
    """

    order_of_magnitude_min = int(np.log10(min(numbers)))
    order_of_magnitude_max = int(np.log10(max(numbers)))

    return order_of_magnitude_min, order_of_magnitude_max
