from scipy.optimize import curve_fit
import uncertainties
from numpy.random import normal


def linear(x, m, q):
    return m * x + q


def fit_parameters(fit_func, xdata, ydata, sigma=None, **curve_fit_opt_args):
    popt, pcov = curve_fit(fit_func, xdata, ydata, sigma=sigma, **curve_fit_opt_args)
    return uncertainties.correlated_values(popt, pcov)


if __name__ == "__main__":
    xs = range(100)
    ys = [0.1 * x + 1. + normal(0, 10) for x in xs]

    print(fit_parameters(linear, xs, ys))
