"""Code for generating categorical and numerical interaction plot

Author: Leodegario Lorenzo II
Date: 28 August 2021
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def categorical_numerical_plot(
        data, numerical_column, categorical_column, y_lim=None):
    """Return plot of categorical and numerical interaction

    Generates two box plot of the given numerical feature. The first
    subplot will be used as a reference plot for the second subplot.
    The second subplot groups the data first according to the
    values of categorical column then generates the box plot of each
    groupings with respect to the numerical column.

    Parameters
    ----------
    data : pandas DataFrame
        Data frame containing the numerical and categorical columns
        whose interaction is to be plotted

    numerical_column : str
        Column to be used as basis for the boxplots

    categorical_column : str
        Column to be used as groupings for the second subplots

    y_lim : tuple, default=None
        Set the y limit of the plot for better readability

    Returns
    -------
    fig, axes : matplotlib Figure and Axes
        Figure and axes of the generate subplots
    """
    # Initialize data frame that enables boxplotting using seaborn
    cur_data = pd.DataFrame()

    # Melt the data frame according to values of categorical_column
    for i, val in enumerate(sorted(set(data[categorical_column]))[::-1]):
        if i == 0:
            cur_data[val] = data.loc[
                data[categorical_column] == val, numerical_column]
        else:
            cur_data = cur_data.append(
                data.loc[data[categorical_column] == val,
                         numerical_column]
                .to_frame(name=val))

    # Initialize figure, width ratios are dependent on the number of
    # categorical values
    fig, axes = plt.subplots(1, 2, figsize=(16, 5.5), sharey=True,
                             gridspec_kw={'width_ratios': [1, i + 1]})

    # Generate reference boxplot
    sns.boxplot(data=data[numerical_column], ax=axes[0])
    sns.boxplot(data=cur_data, ax=axes[1])

    # Prettify figure by setting the ylim, removing unnecessary spines, setting
    # axes labels and ticks
    for ax in axes:
        if y_lim is not None:
            ax.set_ylim(y_lim)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    axes[0].set_ylabel(numerical_column.replace("_", " ").title(), fontsize=14)
    axes[0].set_xticklabels(["ALL"])
    axes[1].set_xlabel(categorical_column.replace("_", " ").title(),
                       fontsize=14)

    return fig, axes
