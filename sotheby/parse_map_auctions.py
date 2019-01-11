import pandas as pd

from sotheby.sotheby_departments import category_from_deps_list

auction_dep_map_file = "/Users/marcomeneghelli/Dropbox (Personal)/W/Education/tesi Giulia/sothebys_csvs/auctions_with_deps.csv"
auction_date_map_file = "/Users/marcomeneghelli/Dropbox (Personal)/W/Education/tesi Giulia/sothebys_csvs/sothebys_auctions.csv"

def calc_and_get_auction_map():
    auction_map = {}

    raw_data_dep = pd.read_csv(auction_dep_map_file)
    column_ids = list(raw_data_dep)[1:]

    for index, row in raw_data_dep.iterrows():
        auction_id = str(row['auction_id'])

        if auction_id not in auction_map:
            auction_map[auction_id] = {'date': None, 'currency': None, 'departments_names': []}

        deps = []
        for column_id in column_ids:
            dep = row[column_id]
            if isinstance(dep, str):
                deps.append(dep)
            else:
                break
        auction_map[auction_id]['departments_names'] = deps
        # break

    for auction_id in auction_map.keys():
        auction_map[auction_id]['category'] = category_from_deps_list(auction_map[auction_id]['departments_names'])

    raw_data_date_cur = pd.read_csv(auction_date_map_file)
    for index, row in raw_data_date_cur.iterrows():
        auction_id = str(row['auction_id'])
        if auction_id not in auction_map:  # TODO uncomment
            continue
        auction_map[auction_id]['date'] = row['datetime'].split('T')[0]
        auction_map[auction_id]['currency'] = row['currency']
        # break

    return auction_map


if __name__ == "__main__":
    map = calc_and_get_auction_map()
    pass

    # """
    # To print unique departments.
    # """
    #
    # raw_data = pd.read_csv(auction_dep_map_file)
    #
    # departments = set()
    #
    # for column_id in list(raw_data)[1:]:
    #     departments = departments.union(set(raw_data[column_id].unique()))
    #
    # print(departments)
