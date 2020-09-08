import matplotlib.pyplot as plt
import numpy as np

from os import listdir


def plot_watchlist(dir_in: str) -> None:
    # Loop over dat ascii files
    for file in listdir(dir_in):
        data = []
        file_path = '%s/%s' % (dir_in, file)
        print(np.loadtxt(file_path))
        with open(file_path, 'r') as f:
            for line in f.readlines():
                # Comma delimited
                data.append(line.strip().split(','))
        plot_data(data)


def plot_data(data: list) -> None:
    # Store list to variables
    x          = [i[0] for i in data]
    cost_low   = [i[1] for i in data]
    cost_high  = [i[2] for i in data]
    price_low  = [i[3] for i in data]
    price_high = [i[4] for i in data]

    fig, ax = plt.subplots()
    ax.plot(x, cost_low,
            x, cost_high,
            x, price_low,
            x, price_high)
    plt.show()


def main():
    plot_watchlist('watchlist')


if __name__ == "__main__":
    main()
