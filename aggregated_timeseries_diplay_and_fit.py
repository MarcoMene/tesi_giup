from os import listdir
import pandas as pd

from auction_calcs import extract_kpis
from christies_departments import art_departments, design_departments
from fitting import fit_parameters, linear
from geometric_brownian_motion_fit import fit_gbm
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


# ** CONFIGURATION

alpha = 0.01
confidence = 1 - alpha

# single fit
currency = 'GBP'
category = 'design' # 'art'  #
kpi = 'avg' # 'money' #

granularity_in_days = YEAR_DAYS # n_months_days(6) #

# ** END CONFIGURATION


date_borders = date_range(min_date, max_date, delta_days=granularity_in_days)
date_borders.append(max_date)

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


# stat analysis
mu_est, mu_err_est, sigma_est = fit_gbm(ys, delta_t_in_years=365/granularity_in_days)

print(" {} - {} - {}".format(currency, category, kpi))

print("(mu_est, mu_err_est, sigma_est) : ({} , {}, {})".format(mu_est, mu_err_est, sigma_est))

t_stat = abs(mu_est) / mu_err_est

print("t-stat (n-sigma): {}".format(t_stat))

p_value = sigma_to_p_value(t_stat)
print("p-value: {}".format(p_value))

if p_value < alpha:
    print(
        "Reject null hypothesis (No trend). So there's a trend.")
else:
    print("Cannot reject null hypothesis")


plot_single_timeseries(ys, x_labels=dates, title=" {} - {} - {}".format(currency, category, kpi), y_label=kpi)
# plot_errorbar_timeseries(ys, ys_err=ys_err, x_labels=dates, title=" {} - {} - {}".format(currency, category, kpi), y_label=kpi)