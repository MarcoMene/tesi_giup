from numpy import log, std, mean, sqrt
from numpy.random import normal, seed


def generate_gbm(mu, sigma, s0=1., N=100, return_diff=False):
    ss = [s0]
    steps = []
    for t in range(1, N + 1):
        prev_s = ss[t - 1]
        step = mu * prev_s + sigma * prev_s * normal()
        ss.append(prev_s + step)
        steps.append(step)
    if return_diff:
        return steps
    return ss


def fit_gbm(xs, delta_t_in_years=1.):
    """
    Fits price-like data with a geometric brownian motion.
    Takes log-returns and extracts the estimates for mu and sigma, with errors.

    Reference: paragraph 3.3 of https://beta.vu.nl/nl/Images/werkstuk-dmouj_tcm235-91341.pdf

    :return: mu, mu_err, sigma
    """
    # take log returns
    log_rs = []
    for i in range(1, len(xs)):
        log_rs.append(log(xs[i] / xs[i - 1]))

    sigma = std(log_rs)
    mu = mean(log_rs) + sigma * sigma / 2
    mu_err = sigma / sqrt(len(log_rs))

    return mu / delta_t_in_years, mu_err / delta_t_in_years, sigma / sqrt(delta_t_in_years)
