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

input_file = "/Users/marcomeneghelli/PycharmProjects/tesi_giup/output_csv/christie_auctions_data.csv"

# sort values by time
timseries_data = pd.read_csv(input_file)
timseries_data['date'] = pd.to_datetime(timseries_data.date)
timseries_data.sort_values(by='date', inplace=True)

currencies = ['USD', 'EUR', 'GBP']

categories = ['art', 'design']

departments = list(art_departments.keys()) + list(design_departments.keys())
departments = [str(d) for d in departments]

kpis = ['avg', 'max', 'median', 'min', 'money', 'std']  # , 'quantile_10', 'quantile_90']  # ,quantile_95]

# single fit  ** CONFIGURATION

aggregated_dataset = []

for currency in currencies:
    for category in categories:
        for department in departments:
            for kpi in kpis:

                current_timeseries = timseries_data[(timseries_data['currency'] == currency) & \
                                                    (timseries_data['category'] == category) & \
                                                    (timseries_data['departments_ids'].str.contains(department))]
                current_timeseries.dropna(inplace=True)

                current_timeseries = current_timeseries[current_timeseries[kpi] > 0]

                ys = list(current_timeseries[kpi])

                timeseries_length = len(ys)
                if timeseries_length < 10:
                    continue

                log_ys = [log10(y) for y in ys]

                # take series of timedelta (in years)
                xs = dates_to_timedelta_in_years(current_timeseries['date'])

                log_fit_result = fit_parameters(linear, xs, log_ys)

                log_m = log_fit_result[0]
                estimate_m, sigma_m = log_m.n, log_m.s

                t_stat = abs(estimate_m) / sigma_m

                p_value = sigma_to_p_value(t_stat)

                ten_to_m = 10 ** log_m
                print("10^m: {} --> {} {}".format(ten_to_m, ten_to_m.n, ten_to_m.s))

                row_to_add = {
                    'currency': currency,
                    'category': category,
                    'department': department,
                    'kpi': kpi,
                    'm': log_m.n,
                    'm_err': log_m.s,
                    'ten_to_m': ten_to_m.n,
                    'ten_to_m_err': ten_to_m.s,
                    't_stat': t_stat,
                    'p_value': p_value,
                }
                aggregated_dataset.append(row_to_add)
    #             break
    #         break
    #     break
    # break

dataset = pd.DataFrame(aggregated_dataset)
dataset.to_csv("output_csv/christie_timeseries_fit_data.csv")
