from os import listdir
import pandas as pd

from christies_departments import department_name_from_id, category_from_ids

files_destination = "/Users/marcomeneghelli/Dropbox (Personal)/W/Education/tesi Giulia/christies_csvs/departments"
filename_prefix = "christie_sales_data_department"


def calc_and_get_auction_map():
    auction_map = {}

    for f in listdir(files_destination):
        print(f)

        dep_id = f.replace(filename_prefix, "").replace("_", "").replace(".csv", "")
        print(dep_id)
        dep_data = pd.read_csv("{}/{}".format(files_destination, f))
        # print(dep_data)

        for index, row in dep_data.iterrows():
            auction_id = str(row['sale_id'])
            date = row['date']

            # remove date rage from date:
            if " - " in date:
                date = date.split(" - ")[1]

            currency = row['currency']

            # print(auction_id, date, currency)

            if auction_id not in auction_map:
                auction_map[auction_id] = {'date': None, 'currency': None, 'departments_ids': [], 'departments_names': []}
            auction_map[auction_id]['date'] = date
            auction_map[auction_id]['currency'] = currency
            auction_map[auction_id]['departments_ids'].append(dep_id)
            auction_map[auction_id]['departments_names'].append(department_name_from_id(dep_id))
        # break

    for auction_id in auction_map.keys():
        auction_map[auction_id]['cartegory'] = category_from_ids(auction_map[auction_id]['departments_ids'])

    # print(auction_map)
    return auction_map
