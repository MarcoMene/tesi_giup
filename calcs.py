

def extract_kpis(auctions_data):
    """

    :param auctions_data: DataFrame with columns 'lot', 'price'
    :return: dictionary with kpis
    """
    res = {}

    res['money'] = auctions_data['price'].sum()
    res['lots_sold'] = auctions_data['lot'].count()
    res['lots_unsold'] = auctions_data['lot'].max() - res['lots_sold']

    res['avg'] = auctions_data['price'].mean()
    res['median'] = auctions_data['price'].median()

    res['quantile_10'] = auctions_data['price'].quantile(q=0.1)
    res['quantile_90'] = auctions_data['price'].quantile(q=0.9)

    res['quantile_95'] = auctions_data['price'].quantile(q=0.95)
    res['max'] = auctions_data['price'].max()
    res['min'] = auctions_data['price'].min()

    res['std'] = auctions_data['price'].std()

    return res



