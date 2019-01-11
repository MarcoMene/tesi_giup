from os import listdir
import pandas as pd

from auction_calcs import extract_kpis
from christies_departments import art_departments, design_departments
from fitting import fit_parameters, linear
from parse_map_auctions import calc_and_get_auction_map
from plotting import plot_single_auction
from numpy import log10, abs
from scipy.stats import norm

from utils import sigma_to_p_value, dates_to_timedelta_in_years

input_file = "/Users/Giulia/bendingspoons/tesi_giup/output_csv/sotheby_auctions_data.csv"
# input_file = "/Users/marcomeneghelli/PycharmProjects/tesi_giup/output_csv/sotheby_auctions_data.csv"

# sort values by time
timseries_data = pd.read_csv(input_file)
timseries_data['date'] = pd.to_datetime(timseries_data.date)
timseries_data.sort_values(by='date', inplace=True)

# set confidence ** CONFIGURATION

alpha = 0.01
confidence = 1 - alpha

# single fit  ** CONFIGURATION
currency = 'USD'
category = 'design'  #
kpi = 'avg'

current_timeseries = timseries_data[(timseries_data['currency'] == currency) &
                                    (timseries_data['category'] == category)
                                    # &  (timseries_data['departments_names'].str.contains('20th Century Design'))  # per vedere singolo dipartimento

                                   &  (  timseries_data['departments_names'].str.contains('American Furniture, Decorative Art & Folk Art') | timseries_data['departments_names'].str.contains('European Ceramics')  | timseries_data['departments_names'].str.contains('English Furniture') | timseries_data['departments_names'].str.contains('French & Continental Furniture') | timseries_data['departments_names'].str.contains('19th Century Furniture & Sculpture') | timseries_data['departments_names'].str.contains('European Sculpture & Works of Art') )  # per vedere piuù dipartimenti

    ]
current_timeseries.dropna(inplace=True)

ys = list(current_timeseries[kpi])
log_ys = [log10(y) for y in ys]

# take series of timedelta (in years)
xs = dates_to_timedelta_in_years(current_timeseries['date'])

log_fit_result = fit_parameters(linear, xs, log_ys)

log_m = log_fit_result[0]
estimate_m, sigma_m = log_m.n, log_m.s

log_q = log_fit_result[1]
estimate_q, sigma_q = log_q.n, log_q.s

t_stat = abs(estimate_m) / sigma_m

print(" {} - {} - {}".format(currency, category, kpi))

print("(m , q) : {}".format(log_fit_result))
print("t-stat (n-sigma): {}".format(t_stat))

p_value = sigma_to_p_value(t_stat)
print("p-value: {}".format(p_value))

ten_to_m = 10 ** log_m
print("10^m: {} --> {} {}".format(ten_to_m, ten_to_m.n, ten_to_m.s))

ten_to_q = 10 ** log_q
print("10^q: {} --> {} {}".format(ten_to_q, ten_to_q.n, ten_to_q.s))

if p_value < alpha:
    print(
        "Reject null hypothesis (No trend). So there's a trend with m: {} , (linear scale {})".format(log_m, ten_to_m))
else:
    print("Cannot reject null hypothesis")
