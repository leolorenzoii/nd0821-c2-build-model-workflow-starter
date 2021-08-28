"""Helper plotter function for categorical to categorical interaction

Author: Leodegario Lorenzo II
Date: 28 August 2021
"""

import pandas as pd
import matplotlib.pyplot as plt


def get_normalized_counts(data, column_1, column_2):
    """Return pivoted data containing the normalize counts of `column_1`

    Groups the data into `column_1` then computes for the proportion of
    the different values of `column_2` per groupings. Returns a data
    frame containing the corresponding percentages per group of
    `column_1` and `column_2`.

    Parameters
    ----------
    data : pandas DataFrame
        Data frame whose percentage frequency groupings is to be
        computed

    column_1 : str
        Column to be used as primary groupings

    column_2 : str
        Column to be used as secondary groupings

    Returns
    -------
    pivot_count : pandas DataFrame
        Dataframe containing the percentage per group of `column_1` and
        `coloumn_2`
    """
    # Pivot data according to column 1 and column 2
    pivoted_data = pd.pivot_table(
        data.groupby([column_1, column_2]).size().to_frame('count')
            .reset_index(),
        values='count',
        index=column_1,
        columns=column_2)

    # Compute for the percentage counts of column 2 as grouped by column 1
    pivot_count = (pivoted_data.divide(pivoted_data.sum(axis=1), axis='index'))

    return pivot_count


def categorical_categorical_plot(data, column_1, column_2):
    """Return fig and axes of interaction of categorical columns 1 and 2

    Two subplots will be created, first a count plot of the values in
    column 1, which will be used as reference during interpretation. The
    second subplot contains the interaction between categorical columns
    1 and 2.

    Parameters
    ----------
    data : pandas DataFrame
        Data frame whose percentage frequency groupings is to be
        computed

    column_1 : str
        Column to be used as primary groupings

    column_2 : str
        Column to be used as secondary groupings

    Returns
    -------
    fig, axes : matplotlib Figure and Axes
        Figure and axes containing the subplots of the categorical vs
        categorical interaction plot
    """
    # Get count data for first subplot, and pivoted data for second plot
    count_data = data.neighbourhood_group.value_counts()
    pivot_count = get_normalized_counts(data, column_1, column_2)
    pivot_count = pivot_count.loc[count_data.index, :]

    # Initialize figure
    fig, axes = plt.subplots(1, 2, figsize=(16, 5.5))

    # Generate count plot and interaction plot
    count_data.plot(kind='bar', ax=axes[0])
    pivot_count.plot(kind='bar', stacked=True, ax=axes[1])

    # Prettify plot by rotating tick parameters, removing spines, placing
    # labels, and setting the location of the legend.
    for ax in axes:
        ax.tick_params(rotation=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel(column_1.replace('_', ' ').title(), fontsize=14)
    axes[0].set_ylabel("Frequency", fontsize=14)
    axes[1].set_ylabel("Percentage", fontsize=14)
    axes[1].legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))

    return fig, axes
