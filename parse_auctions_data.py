from os import listdir
import pandas as pd

from calcs import extract_kpis
from parse_map_auctions import calc_and_get_auction_map
from plotting import plot_single_auction

files_destination = "/Users/marcomeneghelli/Dropbox (Personal)/W/Education/tesi Giulia/christies_csvs"
auctions_subfolder = "auctions"

auctions_folder = "{}/{}".format(files_destination, auctions_subfolder)

auction_prefix = "christie"

auction_map = calc_and_get_auction_map()

aggregated_dataset = []

for f in listdir(auctions_folder):
    print(f)
    auction_id = f.replace(auction_prefix, "").replace("_", "").replace(".csv", "")
    # print(auction_id)
    auctions_data = pd.read_csv("{}/{}".format(auctions_folder, f), header=None, names=['lot', 'price'])
    # print(auctions_data)
    kpis = extract_kpis(auctions_data)

    row_to_add = {}

    row_to_add['auction_id'] = auction_id

    row_to_add.update(kpis)
    row_to_add.update(auction_map[auction_id])

    aggregated_dataset.append(row_to_add)

    # plot_single_auction(auctions_data, logx=True, logy=True, bins=20)
    # break

dataset = pd.DataFrame(aggregated_dataset)
dataset.to_csv("{}_auctions_data.csv".format(auction_prefix))
