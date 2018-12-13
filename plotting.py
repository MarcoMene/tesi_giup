import matplotlib.pyplot as plt

def show_plot():
    print("Enjoy the plot!")
    plt.show()


def plot_single_auction(auctions_data, bins=100, logx=False, logy=False):
    """

    :param auctions_data: DataFrame with columns 'lot', 'price'
    """
    prices = auctions_data['price']

    plt.hist(prices, bins=bins)
    plt.xlabel('{}price'.format("log " if logx else ""))
    plt.ylabel('{}count'.format("log " if logy else ""))

    if logx:
        plt.xscale('log')
    if logy:
        plt.yscale('log')

    show_plot()
