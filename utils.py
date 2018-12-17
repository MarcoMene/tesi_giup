from scipy.stats import norm


def sigma_to_p_value(n_sigma):
    return norm.sf(n_sigma) * 2
