from os import listdir
import pandas as pd

from auction_calcs import extract_kpis
from christies_departments import art_departments, design_departments
from fitting import fit_parameters, linear
from parse_map_auctions import calc_and_get_auction_map
from plotting import plot_single_auction
from numpy import log10


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

# single fit
currency = 'GBP'
category = 'design'
kpi = 'avg'


current_timeseries = timseries_data[ (timseries_data['currency'] == currency) & (timseries_data['category'] == category)]
current_timeseries.dropna(inplace=True)

ys = list(current_timeseries[kpi])
log_ys = [log10(y) for y in ys]
xs = range(len(ys))

print(fit_parameters(linear, xs, ys))
print(fit_parameters(linear, xs, log_ys))
