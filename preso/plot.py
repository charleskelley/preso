"""
Plotting functions with Schwab branding and colors for inclusion in power point
ad other static presentations.
"""
from inspect import ArgInfo
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import namedtuple

from .style import *


def set_theme(**kwargs):
    """
    Set matplotlib and seaborn runtime configuration plot style defaults using
    styling guidance from the official Schwab Brand guidelines website

    Args:
        style (str): one of <white|dark|whitegrid|darkgrid|ticks>
        palette: argument that can be used in seaborn color_palette function
    """   
    style_dict = schwab_axes_style() if "style" not in kwargs else schwab_axes_style(style=kwargs.pop("style"))
    palette = kwargs["palette"] if "palette" in kwargs else scaled_palette()
    sns.set_theme(context="notebook", style=style_dict, palette=palette, **kwargs)
    sns.set_context(rc={"patch.linewidth": 0.0, "grid.linewidth": 0.5})


def figsize(size="defualt"):
    """Set common figure settings sizes for presentation layouts"""
    FIGSIZES = {
        "default": (6, 4),
        "2:1": (8, 4)}
    plt.figure(figsize=FIGSIZES[size], dpi=300)


def savepng(fpath, dpi=600, pad_inches=0, **kwargs):
    """
    Save plot down as PNG image at 600 DPI with no padding. Filepath should
    be first argument and include .png extension.
    """
    plt.savefig(fpath, dpi=dpi, pad_inches=pad_inches, **kwargs)


def mpl_pie(ax, percentages, labels, title=None, **kwargs):
    """Pie plot from set of lists. 
    
    Args:
        ax (obj): matplotlib.axes.Axes object.
        labels (list): Labels for pie slices.
        percentages (list): Percentages of pie for each slice where list length
            and order match labels list.
        **kwargs: All keyword arguments supported by matplotlib axis.pie method.
 
    Note:
        Common kwargs include: 
        explode (list): a len(x) array which specifies the fraction of the
            radius with which to offset each wedge.
        labeldistance (float/None): The radial distance at which the pie labels
            are drawn. If set to None, label are not drawn, but are stored for
            use in matplotlib.axes.Axes.legend() method.
    """
    plt.rcParams["axes.labelcolor"] = "#ffffff"
    plt.rcParams["font.size"] = 14
    ax.pie(
        percentages, labels=labels,
        colors=SCHWAB_PALETTE_HEX[0:len(percentages)],
        autopct="%1.0f%%", **kwargs)
    ax.axis("equal")
    ax.legend(frameon=False, bbox_to_anchor=(1.5, 0.8))
    if title:
        ax.set_title(title)


#############
# BAR PLOTS # 
#############


def stacked_series(df, base, series, pivot=None):
    """
    Create namedtuple StackedSeries from pandas DataFrame that is used to
    create the stacked series in a stacked bar chart. 

    Args:
        df (DataFrame): pandas Dataframe.
        base (str or dict): name of column that will be the base axis for
            stacked barplot if a dict is passed the key column name will be
            renamed with the value.
        series (list or dict): list of column names to build the stacked series
            with. If the pivot option is used, the names should be the
            categorical values in the column used in the column parameter of
            the DataFrame.pivot method. The order items in the list of
            dictionary will be used to order the namedtuple's series attribute
        pivot (dict): dictionary with two items (columns and values) that
            that can be used as arguments to DataFrame.pivot method to flatten
            where the index parameter is assumed to be the column specified in
            the axis argument.

    Returns:
        class: StackedSeries collections.namedtuple instance where the axis
            attribute is the series to be used for the base axis and series is
            the list of series to be stacked in order.
    """
    renames = {}
    if isinstance(base, dict):
        renames.update(base)
        base_col = list(base.values())[0]
        index = list(base.keys())[0]
    else:
        base_col = base 
        index = base
    if isinstance(series, dict):
        renames.update(series)
        series_cols = series.values()
    else:
        series_cols = series
        
    if pivot:
        df = df.pivot(
            index=index, columns=pivot["columns"],
            values=pivot["values"]).reset_index()
        
    if renames:
        df.rename(columns=renames, inplace=True)

    StackedSeries = namedtuple("StackedSeries", ["base", "series"])
    return StackedSeries(df[base_col], [df[s] for s in series_cols])


def sum_series(index, series):
    """
    Create a series that is the sum of all previous series that to be used as
    the bottom of the next category in the series stack.
    
    Args:
        index (int): index in tuple of series.
        series (tuple): tuple of named series that will be stacked. 
    """
    bottom = [0] * len(series[0])
    for i in range(0, index):
        bottom = np.add(bottom, series[i])
    return bottom


def stack_bars(stack, ax=None, **kwargs):
    """
    Add each series in stack to matplotlib axes where each the bottom of each
    subsequent series is the sum of the previouse series.

    Args:
        ax (obj): matplotlib.axes.Axes object.
        stack (tuple): tuple of named series to iterate over and stack from
            bottom to top 0 to N.
    """
    ax = plt.gca() if ax is None else ax
    for i, s in enumerate(stack.series):
        if i == 0:
            ax.bar(stack.base, s, label=s.name, **kwargs)
        else:
            ax.bar(
                stack.base, s, bottom=sum_series(i, stack.series),
                label=s.name, **kwargs)
    ax.legend(
        ncol=len(stack.series), loc="lower center",
        bbox_to_anchor=(0.5, -0.2), fontsize="x-small")


def stackbar(df, base, series, pivot=None, hbar=False, ax=None, size="default", **kwargs):
    """Draw a stacked bar chart by layering series on top of one another.
    
    Args:
        df (DataFrame): pandas DataFrame with data to be plotted.
        base (str|dict): name of column used for the base categorical axis.
        series (str, list, or dict): string name of column that contains
            categories for the bar series to be stacked, list of column names
            whose series will be plotted, or dictionary.
        pivot (dict): dictionary with two items (columns and values) that
            that can be used as arguments to DataFrame.pivot method to flatten
            where the index parameter is assumed to be the column specified in
            the axis argument.
        hbar (bool): create a horizontal bar chart if true, vertical is default.

    Returns:
        matplotlib.axes.Axes
    """
    # Plot configuration
    sides = {"left": True, "right": True, "bottom": True, "top": True}
    base_side = "bottom" if not hbar else "left"
    set_theme()
    figsize(size)

    # Draw plot
    stack = stacked_series(df, base, series, pivot=pivot)
    ax = stack_bars(stack, ax=ax, **kwargs)

    # Style newly drawn Axes
    sns.despine(**sides)
    thin_spine_style(side=base_side, ax=ax)
    tight_tick_params(ax=ax)
    rotate30_xaxis(ax=ax)


def line(
    df, x, y, size="default", style="FiveThirtyEight",
    rotate_xlabel=False, ax=None, **kwargs):
    """Draw a line plot using seaborn.lineplot().
 
    Args:
        df (DataFrame): pandas DataFrame with data to be plotted.
        x (str): column name from df to be used on x-axis.
        y (str): column name from df to be used on y-axis.
        **kwargs (varies): key value parameters accepted by the sns.lineplot
            method and by extension the matplotlib.axes.Axes.plot().
    """
    # Plot configuration
    set_theme(style=style)
    figsize(size)

    # Draw plot
    ax = sns.lineplot(x, y, data=df, **kwargs)

    # Style newly drawn Axes
    ax.set(xlabel=None, ylabel=None)
    sns.despine(left=True)
    thin_spine_style(ax=ax)
    tight_tick_params(ax=ax)

    if rotate_xlabel:
        rotate30_xaxis(ax=ax)
    ax.legend(
        ncol=4, loc="lower center",
        bbox_to_anchor=(0.5, -0.2), fontsize="x-small")


def stripplot(df, x, y, **kwargs):
    """Draw stripplot using seaborn.stripplot().

    Args:
        df (DataFrame): pandas DataFrame with data to be plotted.
        x (str): column name from df to be used on x-axis.
        y (str): column name from df to be used on y-axis.
    
    """
    palette = rgb_scaled(plot.SCHWAB_PALETTE_RGB) if palette not in kwargs else kwargs["palette"]
    sns.stripplot(x=x, y=y, data=df, **kwargs)


