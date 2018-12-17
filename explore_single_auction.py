from os import listdir
import pandas as pd

from auction_calcs import extract_kpis
from parse_map_auctions import calc_and_get_auction_map
from plotting import plot_single_auction

files_destination = "/Users/marcomeneghelli/Dropbox (Personal)/W/Education/tesi Giulia/christies_csvs"
auctions_subfolder = "auctions"

auctions_folder = "{}/{}".format(files_destination, auctions_subfolder)

auction_prefix = "christie"

auction_map = calc_and_get_auction_map()

auction_id = "26830"

f = "{}_{}.csv".format(auction_prefix, auction_id)

auctions_data = pd.read_csv("{}/{}".format(auctions_folder, f ), header=None, names=['lot', 'price'])
print(auctions_data)
kpis = extract_kpis(auctions_data)
print(kpis)

plot_single_auction(auctions_data, logx=False, logy=False, bins=100,
                    title="{} - auction {}".format(auction_prefix, auction_id))

