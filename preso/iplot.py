"""
Plotting functions with Schwab branding and colors  
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import namedtuple

from .style import *


def add_labels(extra_labels, **kwargs):
    """
    Creates consolidated label dictionary by adding variable dictionary key
    value pairs to the labels dictionary for plot axes and legend variable
    renaming 
    """
    if not isinstance(extra_labels, dict):
        raise TypeError("extra_labels argrument must be dict object")
    if kwargs and "labels" not in kwargs:
        kwargs["labels"] = {}
    kwargs["labels"] = {**kwargs["labels"], **extra_labels}
    return kwargs


def axes_vars(axes_vars):
    """Returns namedtuple AxesVars with x and y variable string column names"""
    AxesVars = namedtuple("AxesVars", ["x", "y"])
    if isinstance(axes_vars, list):
        return AxesVars(axes_vars[0], axes_vars[1])
    elif isinstance(axes_vars, dict):
        var_list = axes_vars.keys()
        return AxesVars(var_list[0], var_list[1])
    else:
        raise TypeError("axes_vars argument must be list or dict object")


def px_pie(
    data_frame, names, values, color_discrete_sequence=INFO_DESIGN_PALETTE,
    showlegend=False, **kwargs):
    """plotly.express.pie() plot with Schwab brand styling

    Args:
        data_frame (DataFrame): pandas.DataFrame object with at least two
            columns to serve as names and values arguments.
        names (str or dict): Column name from data_frame used as pie chart
            slice names. If a dict is used it should be a key: value pair of
            strings (){'names_col': 'Col Alias Label'}) where the value is used
            as an alias label in the figure.
        values (str/dict): Column name from df used as values to determine
            percentage of total for given slice.
        color_discrete_sequence (list of str): List of string color values.
            Strings should define valid CSS-colors. If the the list lenth is
            shorter than the number of elements in the category the color is
            applied to, the list will be cycled.
        showlegend (bool): True/False to show color legend for named slices
            where False is the default.
        **kwargs: Any keyword arguments for plotly.express.pie() method.

    Returns:
        plotly.graph_objects.Figure
    """
    fig = px.pie(
        data_frame=data_frame, names=names, values=values,
        color_discrete_sequence=color_discrete_sequence, **kwargs)
    fig.update_traces(textinfo="percent+label+value", showlegend=showlegend)
    return fig 


def px_bar(
    data_frame, xy_vars, color_discrete_sequence=INFO_DESIGN_PALETTE,
    showlegend=False, **kwargs):
    """plotly.express.pie() plot with Schwab brand styling

    Args:
        data_frame (DataFrame): pandas.DataFrame object with at least two
            columns to serve as x and y variables.
        xy_cols (list/dict of str): Column names ['x', 'y'] from data_frame
            used as pie chart slice names.
        values (str): Column name from df used as values to determine
            percentage of total for given slice.
        **kwargs: Any keyword arguments for plotly.express.bar() method.

    Returns:
        plotly.graph_objects.Figure
    """
    xyvars = axes_vars(xy_vars) 
    xvar, yvar = xyvars.x, xyvars.y
    fig = px.bar(
        data_frame=data_frame, x=xvar, y=yvar,
        color_discrete_sequence=color_discrete_sequence, **kwargs)
    fig.update_layout(showlegend=showlegend)
    return fig



