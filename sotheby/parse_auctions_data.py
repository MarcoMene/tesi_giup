from os import listdir
import pandas as pd

from auction_calcs import extract_kpis
from parse_map_auctions import calc_and_get_auction_map
from plotting import plot_single_auction
import numpy as np

files_destination = "/Users/marcomeneghelli/Dropbox (Personal)/W/Education/tesi Giulia/sothebys_csvs"
auctions_subfolder = "auctions"

auctions_folder = "{}/{}".format(files_destination, auctions_subfolder)

auction_map = calc_and_get_auction_map()

aggregated_dataset = []

for f in listdir(auctions_folder):
    # print(f)
    auction_id = f.replace(".csv", "")
    print(auction_id)
    auctions_data = pd.read_csv("{}/{}".format(auctions_folder, f), header=0, names=['lot', 'price'])

    prices = auctions_data['price']
    if prices.dtype == float:
        prices = prices * 1000
    else:
        prices = prices.str.replace('.', '', regex=False)
        prices = prices.astype(np.float)
    auctions_data['price'] = prices

    # print(auctions_data)
    kpis = extract_kpis(auctions_data)

    row_to_add = {}

    if auction_id not in auction_map:
        continue

    row_to_add['auction_id'] = auction_id

    row_to_add.update(kpis)
    row_to_add.update(auction_map[auction_id])

    aggregated_dataset.append(row_to_add)

    # plot_single_auction(auctions_data, logx=True, logy=True, bins=20)
    # break

dataset = pd.DataFrame(aggregated_dataset)
dataset.to_csv("output_csv/sotheby_auctions_data.csv")
