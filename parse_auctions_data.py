from os import listdir
import pandas as pd

from calcs import extract_kpis
from plotting import plot_single_auction

files_destination = "/Users/marcomeneghelli/Dropbox (Personal)/W/Education/tesi Giulia/christies_csvs"
auctions_subfolder = "auctions"

auctions_folder = "{}/{}".format(files_destination, auctions_subfolder)

auction_prefix = "christie"

for f in listdir(auctions_folder):
    print(f)
    auction_id = f.replace(auction_prefix, "").replace("_", "").replace(".csv", "")
    print(auction_id)
    auctions_data = pd.read_csv("{}/{}".format(auctions_folder, f), header=None, names=['lot', 'price'])
    print(auctions_data)
    print(extract_kpis(auctions_data))

    # plot_single_auction(auctions_data, logx=True, logy=True, bins=20)
    break

