from os import listdir
import pandas as pd

from auction_calcs import extract_kpis
from christies_departments import art_departments, design_departments
from fitting import fit_parameters, linear
from parse_map_auctions import calc_and_get_auction_map
from plotting import plot_single_auction, plot_single_timeseries, plot_errorbar_timeseries
from numpy import log10, abs, sqrt
from scipy.stats import norm
from utils import date_range, date_to_str

from utils import sigma_to_p_value, dates_to_timedelta_in_years

input_file = "/Users/marcomeneghelli/PycharmProjects/tesi_giup/output_csv/christie_auctions_data.csv"

# sort values by time
timseries_data = pd.read_csv(input_file)
timseries_data['date'] = pd.to_datetime(timseries_data.date)
timseries_data.sort_values(by='date', inplace=True)

min_date = timseries_data['date'].min()
max_date = timseries_data['date'].max()

YEAR_DAYS = 365

def n_months_days(n):
    return n * 31

date_borders = date_range(min_date, max_date, delta_days=YEAR_DAYS)
date_borders.append(max_date)

# ** CONFIGURATION

alpha = 0.05
confidence = 1 - alpha

# single fit
currency = 'GBP'
category = 'art'  # 'design' #
kpi = 'avg' # 'money' #

# ** END CONFIGURATION


# extract and clean data
current_timeseries = timseries_data[(timseries_data['currency'] == currency) & (timseries_data['category'] == category)]
current_timeseries.dropna(inplace=True)


# create aggregated timeseries
dates = [date_to_str(d) for d in date_borders[:-1]]
ys = []
ys_err = []


for i in range(len(date_borders) - 1):
    cur_date = date_borders[i]
    next_date = date_borders[i+1]

    partial_timeseries = current_timeseries[(current_timeseries['date'] >= cur_date)
                                            & (current_timeseries['date'] <= next_date)]

    ys.append(partial_timeseries[kpi].mean())
    # ys_err.append(partial_timeseries[kpi].std() / sqrt(partial_timeseries[kpi].count()) )
    # ys.append(partial_timeseries[kpi].sum())


# TODO: setup a geometric brownian motion fit

# stat analysis

# log_ys = [log10(y) for y in ys]
#
# # take series of timedelta (in years)
# xs = dates_to_timedelta_in_years(current_timeseries['date'])
#
# log_fit_result = fit_parameters(linear, xs, log_ys)
#
# log_m = log_fit_result[0]
# estimate_m, sigma_m = log_m.n, log_m.s
#
# t_stat = abs(estimate_m) / sigma_m
#
# print(" {} - {} - {}".format(currency, category, kpi))
#
# print("(m , q) : {}".format(log_fit_result))
# print("t-stat (n-sigma): {}".format(t_stat))
#
# p_value = sigma_to_p_value(t_stat)
# print("p-value: {}".format(p_value))
#
# ten_to_m = 10 ** log_m
# print("10^m: {} --> {} {}".format(ten_to_m, ten_to_m.n, ten_to_m.s))
#
# if p_value < alpha:
#     print(
#         "Reject null hypothesis (No trend). So there's a trend with m: {} , (linear scale {})".format(log_m, ten_to_m))
# else:
#     print("Cannot reject null hypothesis")


plot_single_timeseries(ys, x_labels=dates, title=" {} - {} - {}".format(currency, category, kpi), y_label=kpi)
# plot_errorbar_timeseries(ys, ys_err=ys_err, x_labels=dates, title=" {} - {} - {}".format(currency, category, kpi), y_label=kpi)