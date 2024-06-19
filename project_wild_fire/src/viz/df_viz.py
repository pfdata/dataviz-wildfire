import pandas as pd
import matplotlib.pyplot as plt


class DataFrameVisualizer:

    def __init__(self, df):
        self.df = df

    def plot_histogram(
        self, column, bins=10, title=None, xlabel=None, ylabel="Frequency"
    ):
        plt.figure(figsize=(10, 6))
        plt.hist(self.df[column], bins=bins, edgecolor="black")
        title = title if title else f"Histogram of {column}"
        plt.title(title)
        xlabel = xlabel if xlabel else column
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
        plt.close()

    def plot_scatter(self, x_column, y_column, title=None, xlabel=None, ylabel=None):
        plt.figure(figsize=(20, 10))
        plt.scatter(self.df[x_column], self.df[y_column])
        title = title if title else f"Scatter Plot of {x_column} vs {y_column}"
        plt.title(title)
        xlabel = xlabel if xlabel else x_column
        plt.xlabel(xlabel)
        ylabel = ylabel if ylabel else y_column
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()
        plt.close()
