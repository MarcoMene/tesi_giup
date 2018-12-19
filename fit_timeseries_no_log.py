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


input_file = "/Users/Giulia/bendingspoons/tesi_giup/output_csv/christie_auctions_data.csv"

# sort values by time
timseries_data = pd.read_csv(input_file)
timseries_data['date'] = pd.to_datetime(timseries_data.date)
timseries_data.sort_values(by='date', inplace=True)


alpha = 0.01
confidence = 1 - alpha




# single fit  ** CONFIGURATION
currency = 'GBP'
category = 'design' # 'art' #

current_timeseries = timseries_data[ (timseries_data['currency'] == currency) & (timseries_data['category'] == category)]
current_timeseries.dropna(inplace=True)

# percentuale di lotti invenduti
#ys = list(  current_timeseries['lots_unsold']/(current_timeseries['lots_unsold'] + current_timeseries['lots_sold']) )

#lottiin palio
ys = list(  current_timeseries['lots_unsold'] + current_timeseries['lots_sold'])

# take series of timedelta (in years)
xs = dates_to_timedelta_in_years(current_timeseries['date'])


# fit_result = fit_parameters(linear, xs, ys)

fit_result = fit_parameters(linear, xs, ys)

m = fit_result[0]
estimate_m, sigma_m = m.n, m.s

t_stat = abs(estimate_m) / sigma_m


print(" {} - {} - {}".format(currency, category, "percentage of lots unsold"))

print("(m , q) : {}".format(fit_result))
print("t-stat (n-sigma): {}".format(t_stat))

p_value = sigma_to_p_value(t_stat)
print("p-value: {}".format(p_value))

print("1m: {} --> {} {}".format(m, m.n, m.s))

if p_value < alpha:
    print("Reject null hypothesis (No trend). So there's a trend with m: {}".format(m))
else:
    print("Cannot reject null hypothesis")