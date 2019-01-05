from os import listdir
import pandas as pd
import numpy as np

from auction_calcs import extract_kpis
from plotting import plot_single_auction

auctions_folder = "/Users/marcomeneghelli/Dropbox (Personal)/W/Education/tesi Giulia/sothebys_csvs/auctions"

auction_id = "L10033"  # <-- cambia questo per cambiare asta

f = "{}.csv".format(auction_id)

auctions_data = pd.read_csv("{}/{}".format(auctions_folder, f ), header=0, names=['lot', 'price'])

prices = auctions_data['price']
if prices.dtype == float:
    prices = prices*1000
else:
    prices = prices.str.replace('.', '', regex=False)
    prices = prices.astype(np.float)
auctions_data['price'] = prices

print(auctions_data)
kpis = extract_kpis(auctions_data)
print(kpis)

plot_single_auction(auctions_data, logx=False, logy=True, bins=150,
                    title="Sotheby's - auction {}".format(auction_id))

