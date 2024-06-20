import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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

    def plot_scatter(
        self, x_column, y_column, title=None, xlabel=None, ylabel=None, plot_avg=False
    ):
        plt.figure(figsize=(20, 10))
        plt.scatter(self.df[x_column], self.df[y_column])
        title = title if title else f"Scatter Plot of {x_column} vs {y_column}"
        plt.title(title)
        xlabel = xlabel if xlabel else x_column
        plt.xlabel(xlabel)
        ylabel = ylabel if ylabel else y_column
        plt.ylabel(ylabel)
        y_avg = self.df[y_column].mean()
        x_min = self.df[x_column].min()
        x_max = self.df[x_column].max()
        y_max = self.df[y_column].max()
        y_min = self.df[y_column].min()
        max_row = self.df.loc[self.df[y_column].idxmax()]

        max_land = max_row["Land"].iloc[0]

        if plot_avg:

            plt.plot(
                [x_min, x_max], [y_avg, y_avg], color="r", linestyle="--", linewidth=1
            )
            plt.scatter(
                x_max, y_avg, color="red"
            )  # Point at the maximum x and average y
            plt.text(
                x_max,
                y_avg,
                f"  Avg: {y_avg:.2f}",
                color="red",
                verticalalignment="bottom",
            )
        plt.scatter(x_max, y_max, color="green", s=100)  # Larger point for emphasis
        plt.text(
            x_max,
            y_max,
            f"Max: {x_max}: {y_max} ({max_land})",
            color="green",
            verticalalignment="bottom",
        )

        plt.show()
        plt.close()

    def lineplot(self):
        # Set up the figure and axes
        plt.figure(figsize=(14, 8))

        # Example: Plotting trends for 'Vorsatz (Brandstiftung) Anzahl'
        sns.lineplot(
            data=self.df,
            x="Land",
            y="Vorsatz (Brandstiftung) Anzahl",
            marker="o",
            label="Vorsatz (Brandstiftung) Anzahl",
        )

        # Adding labels and title
        plt.xlabel("Bundesland")
        plt.ylabel("Anzahl")
        plt.title("Trends in Vorsatz (Brandstiftung) Anzahl across Bundesländer")

        # Rotating x-axis labels for better readability
        plt.xticks(rotation=45, ha="right")

        # Display the plot
        plt.tight_layout()
        plt.legend()
        plt.show()
