from scipy.stats import norm


import datetime
from six import string_types

DATE_FORMAT = '%Y-%m-%d'  # DO NOT CHANGE THIS!


YEAR_SECONDS = 86400*365



def sigma_to_p_value(n_sigma):
    return norm.sf(n_sigma) * 2


def dates_to_timedelta_in_years(dates):
    min_time = dates.min()
    time_deltas = (dates - min_time)
    return [td.total_seconds() / YEAR_SECONDS for td in time_deltas]


def is_string(a_string):
    return isinstance(a_string, string_types)


def today():
    return datetime.datetime.utcnow().strftime(DATE_FORMAT)


def yesterday():
    return (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime(DATE_FORMAT)


def add_days(date_as_string, n_days=1):
    date = str_to_date(date_as_string)
    if date is None:
        return None
    next_date = date + datetime.timedelta(days=n_days)
    return date_to_str(next_date)


def str_to_date(date_as_string):
    if not date_as_string:
        return None
    if isinstance(date_as_string, datetime.datetime):
        return date_as_string
    elif isinstance(date_as_string, datetime.date):
        return date_as_string
    return datetime.datetime.strptime(date_as_string, DATE_FORMAT)


def date_to_str(date_as_date):
    if not date_as_date:
        return None
    if is_string(date_as_date):
        return date_as_date
    return date_as_date.strftime(DATE_FORMAT)


def date_diff_in_days(d1, d2):
    """
    Gets number of days between two dates as d1 - d2
    :type d1:   datetime.datetime, str
    :type d2:   datetime.datetime, str
    :return:    days between
    """
    return _date_diff(d1, d2).days


def _date_diff(d1, d2):
    d1 = str_to_date(d1)
    d2 = str_to_date(d2)

    return (d1 - d2)


def date_diff_in_weeks(d1, d2):
    return date_diff_in_days(d1, d2) // 7


def date_diff_in_months(d1, d2):
    return date_diff_in_days(d1, d2) // 31


def date_range(start, end, delta_days=1, return_as_strings=False):
    """
    Create an array of dates comprised between start and end
    :type start: datetime.date, str
    :type end: datetime.date, str
    :param delta_days: number of days between each date
    :type delta_days: int
    """
    if end < start:
        raise ValueError(
            "end date minor than start date.. Maybe you want to swap them? [" + str(start) + ", " + str(end) + "]")

    if is_string(start):
        start = str_to_date(start)
    if is_string(end):
        end = str_to_date(end)
    r = (end - start).days  # + datetime.timedelta(days=1)
    if return_as_strings:
        return [date_to_str(start + datetime.timedelta(days=i * delta_days)) for i in
                range(r // delta_days + 1)]
    return [start + datetime.timedelta(days=i * delta_days) for i in range(r // delta_days + 1)]
