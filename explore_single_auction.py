from os import listdir
import pandas as pd

from auction_calcs import extract_kpis
from plotting import plot_single_auction

files_destination = "/Users/Giulia/Desktop/Data for Thesis/christies_csvs"

auctions_folder = files_destination

auction_prefix = "christie"

auction_id = "27244"  # <-- cambia questo per cambiare asta

f = "{}_{}.csv".format(auction_prefix, auction_id)

auctions_data = pd.read_csv("{}/{}".format(auctions_folder, f ), header=None, names=['lot', 'price'])
print(auctions_data)
kpis = extract_kpis(auctions_data)
print(kpis)

plot_single_auction(auctions_data, logx=False, logy=True, bins=150,
                    title="{} - auction {}".format(auction_prefix, auction_id))

