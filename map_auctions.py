from os import listdir
from os.path import isfile, join
import pandas as pd

from calcs import extract_kpis
from plotting import plot_single_auction

files_destination = "/Users/marcomeneghelli/Dropbox (Personal)/W/Education/tesi Giulia/christies_csvs/departments"

for f in listdir(files_destination):
    print(f)

