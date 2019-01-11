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

input_file = "/Users/marcomeneghelli/PycharmProjects/tesi_giup/output_csv/sotheby_auctions_data.csv"

# sort values by time
timseries_data = pd.read_csv(input_file)
timseries_data['date'] = pd.to_datetime(timseries_data.date)
timseries_data.sort_values(by='date', inplace=True)

# set confidence ** CONFIGURATION

alpha = 0.01
confidence = 1 - alpha

# single fit  ** CONFIGURATION
currency = 'USD'
category = 'design'  # 'art' #

current_timeseries = timseries_data[(timseries_data['currency'] == currency) &
                                    (timseries_data['category'] == category)
                                    #  &  (timseries_data['departments_ids'].str.contains('29'))  # per vedere singolo dipartimento

                                    #&  (  timseries_data['departments_ids'].str.contains('29') | timseries_data['departments_ids'].str.contains('74')  | timseries_data['departments_ids'].str.contains('111') )  # per vedere piuù dipartimenti

    ]
current_timeseries.dropna(inplace=True)

# percentuale di lotti invenduti
# ys = list(  current_timeseries['lots_unsold']/(current_timeseries['lots_unsold'] + current_timeseries['lots_sold']) )

# lottiin palio
ys = list(current_timeseries['lots_unsold'] + current_timeseries['lots_sold'])

# take series of timedelta (in years)
xs = dates_to_timedelta_in_years(current_timeseries['date'])

fit_result = fit_parameters(linear, xs, ys)

m = fit_result[0]
estimate_m, sigma_m = m.n, m.s

q = fit_result[1]
estimate_q, sigma_q = q.n, q.s

t_stat = abs(estimate_m) / sigma_m

# t_stat_ten_to_m = abs(ten_to_m.n - 1) / ten_to_m.s
# p_value_ten_to_m = sigma_to_p_value(t_stat_ten_to_m)
# print("t-stat  ten_to_m (n-sigma): {}".format(t_stat_ten_to_m))
# print("p-value ten_to_m: {}".format(p_value_ten_to_m))

print(" {} - {} - {}".format(currency, category, kpi))

print("(m , q) : {}".format(fit_result))
print("t-stat (n-sigma): {}".format(t_stat))

p_value = sigma_to_p_value(t_stat)
print("p-value: {}".format(p_value))


if p_value < alpha:
    print(
        "Reject null hypothesis (No trend). So there's a trend with m: {} )".format(m))
else:
    print("Cannot reject null hypothesis")
