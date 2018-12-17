from scipy.stats import norm

YEAR_SECONDS = 86400*365


def sigma_to_p_value(n_sigma):
    return norm.sf(n_sigma) * 2


def dates_to_timedelta_in_years(dates):
    min_time = dates.min()
    time_deltas = (dates - min_time)
    return [td.total_seconds() / YEAR_SECONDS for td in time_deltas]

