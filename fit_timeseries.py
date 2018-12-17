from os import listdir
import pandas as pd

from auction_calcs import extract_kpis
from christies_departments import art_departments, design_departments
from fitting import fit_parameters, linear
from parse_map_auctions import calc_and_get_auction_map
from plotting import plot_single_auction
from numpy import log10, abs
from scipy.stats import norm

from utils import sigma_to_p_value

YEAR_SECONDS = 86400*365


input_file = "/Users/marcomeneghelli/PycharmProjects/tesi_giup/output_csv/christie_auctions_data.csv"

# sort values by time
timseries_data = pd.read_csv(input_file)
timseries_data['date'] = pd.to_datetime(timseries_data.date)
timseries_data.sort_values(by='date', inplace=True)

currencies = ['USD', 'EUR', 'GBP']

categories = ['art', 'design']

departments = list(art_departments.keys()) + list(design_departments.keys())
departments = [str(d) for d in departments]

kpis = ['avg', 'max', 'median', 'min', 'money', 'quantile_10', 'quantile_90']  # ,quantile_95,std]


# aggregated_dataset = []



alpha = 0.05
confidence = 1 - alpha




# single fit  ** CONFIGURATION
currency = 'GBP'
category = 'art' # 'design' #
kpi = 'median'


current_timeseries = timseries_data[ (timseries_data['currency'] == currency) & (timseries_data['category'] == category)]
current_timeseries.dropna(inplace=True)

ys = list(current_timeseries[kpi])
log_ys = [log10(y) for y in ys]

# take series of timedelta (in years)
min_time = current_timeseries['date'].min()
time_deltas = (current_timeseries['date'] - min_time)
xs = [td.total_seconds()/YEAR_SECONDS for td in time_deltas]


# fit_result = fit_parameters(linear, xs, ys)

log_fit_result = fit_parameters(linear, xs, log_ys)

log_m = log_fit_result[0]
estimate_m, sigma_m = log_m.n, log_m.s

t_stat = abs(estimate_m) / sigma_m


print(" {} - {} - {}".format(currency, category, kpi))

print("(m , q) : {}".format(log_fit_result))
print("t-stat (n-sigma): {}".format(t_stat))

p_value = sigma_to_p_value(t_stat)
print("p-value: {}".format(p_value))

ten_to_m = 10 ** log_m
print("10^m: {} --> {} {}".format(ten_to_m, ten_to_m.n, ten_to_m.s))

if p_value < alpha:
    print("Reject null hypothesis (No trend). So there's a trend with m: {} , (linear scale {})".format(log_m, ten_to_m))
else:
    print("Cannot reject null hypothesis")