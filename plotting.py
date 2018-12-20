import matplotlib.pyplot as plt


def show_plot():
    print("Enjoy the plot!")
    plt.show()


def plot_single_auction(auctions_data, bins=100, logx=False, logy=False, title=""):
    """

    :param auctions_data: DataFrame with columns 'lot', 'price'
    """
    prices = auctions_data['price']

    plt.hist(prices, bins=bins)
    plt.title(title)
    plt.xlabel('{}price'.format("log " if logx else ""))
    plt.ylabel('{}count'.format("log " if logy else ""))

    if logx:
        plt.xscale('log')
    if logy:
        plt.yscale('log')

    show_plot()


def plot_single_timeseries(ys, xs=None, logy=False, title="", y_label="", x_labels=None):
    """

    :param auctions_data: DataFrame with columns 'lot', 'price'
    """

    if xs is None:
        xs = list(range(len(ys)))

    plt.scatter(xs, ys)
    plt.title(title)
    plt.ylabel('{} {}'.format("log " if logy else "", y_label))

    if logy:
        plt.yscale('log')

    if x_labels is not None:
        plt.xticks(xs,x_labels, rotation=20)
    show_plot()


def plot_errorbar_timeseries(ys, ys_err, xs=None, logy=False, title="", y_label="", x_labels=None):
    """

    :param auctions_data: DataFrame with columns 'lot', 'price'
    """

    if xs is None:
        xs = list(range(len(ys)))

    plt.errorbar(xs, ys, yerr=ys_err)
    plt.title(title)
    plt.ylabel('{} {}'.format("log " if logy else "", y_label))

    if logy:
        plt.yscale('log')

    if x_labels is not None:
        plt.xticks(xs,x_labels,
                   rotation=20
                   )

    show_plot()
