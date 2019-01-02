from numpy.random import seed, normal
import numpy as np
from geometric_brownian_motion_fit import generate_gbm, fit_gbm, correlation_returns


def test_fit_gbm():
    seed(10)

    mu = 0.05
    sigma = 0.1

    ss = generate_gbm(mu, sigma, N=100)

    mu_est, mu_err_est, sigma_est = fit_gbm(ss)

    assert mu > 0.04 and mu_est < 0.06
    assert mu_err_est > 0.0001 and mu_err_est < 0.02
    assert sigma_est > 0.08 and sigma_est < 0.11


def test_correlation_returns():
    seed(10)

    mu = 0.0
    sigma = 0.1

    xs = generate_gbm(mu, sigma, N=100)
    ys = generate_gbm(mu, sigma, N=100)

    cc = correlation_returns(xs, ys)

    print(cc, fit_gbm(xs), fit_gbm(ys))

    assert cc < 0.2

    mu = 0.1
    sigma = 0.1

    xs = generate_gbm(mu, sigma, N=100)
    ys = list(np.array(xs) + normal(scale=sigma, size=101))

    cc = correlation_returns(xs, ys)

    print(cc, fit_gbm(xs), fit_gbm(ys))

    assert cc > 0.6




