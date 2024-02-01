# Data Lifecycle: Visualization.
# Using Seaborn and matplotlib to graph data.

import seaborn
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    filename = input("Enter CSV file name: ")

    # Seaborn has its own functions for reading CSVs into weakly-typed "data frames".
    all_readings = pd.read_csv(filename)

    # Show a line plot of temperature over each day in the readings.
    seaborn.lineplot(data=all_readings, x=list(range(len(all_readings))), y="Temperature")
    plt.show()
