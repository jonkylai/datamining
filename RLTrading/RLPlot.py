from RLUtil import TIME_FORMAT, WATCH_DIR

import matplotlib.pyplot as plt

from matplotlib.ticker import FormatStrFormatter
from datetime import datetime
from os import listdir


def plot_watchlist(dir_in: str) -> None:
    # Loop over dat ascii files
    for file in listdir(dir_in):

        # Only process .dat files
        if '.dat' in file:
            data = []
            file_path = '%s/%s' % (dir_in, file)
            with open(file_path, 'r') as f:
                for line in f.readlines():
                    # Comma delimited
                    data.append(line.strip().split(','))

            # Save each figure
            plot_data(file, data)


def plot_data(filename: str, data: list) -> None:
    # Store list to variables
    t      = [ datetime.strptime(i[0], TIME_FORMAT) for i in data ]
    c_low  = [ float(i[1]) for i in data ]
    c_high = [ float(i[2]) for i in data ]
    p_low  = [ float(i[3]) for i in data ]
    p_high = [ float(i[4]) for i in data ]

    # Plot aesthetics
    fig, ax = plt.subplots()
    cost_low   = ax.plot(t, c_low, label='Cost Low')
    cost_high  = ax.plot(t, c_high, label='Cost High')
    price_low  = ax.plot(t, p_low, label='Price Low')
    price_high = ax.plot(t, p_high, label='Price High')
    ax.legend(loc='upper left')

    plt.title(filename)

    # X-Axis
    plt.xlabel('Date')
    plt.xticks(rotation=90)

    # Y-Axis
    plt.ylabel('Value')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%i'))

    # Save image
    image_out = '%s/%s.png' % (WATCH_DIR, filename.split('.dat')[0])
    fig.set_size_inches(12, 10)
    fig.savefig(image_out, dpi=100)
    print('Saved image to %s' % image_out)


def main():
    plot_watchlist(WATCH_DIR)
    print('Done')


if __name__ == "__main__":
    main()
