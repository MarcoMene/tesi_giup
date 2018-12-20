from numpy.random import seed
from geometric_brownian_motion_fit import generate_gbm, fit_gbm


def test_fit_gbm():
    seed(10)

    mu = 0.05
    sigma = 0.1

    ss = generate_gbm(mu, sigma, N=100)

    mu_est, mu_err_est, sigma_est = fit_gbm(ss)

    assert mu > 0.04 and mu_est < 0.06
    assert mu_err_est > 0.0001 and mu_err_est < 0.02
    assert sigma_est > 0.08 and sigma_est < 0.11
