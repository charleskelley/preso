"""
Setup matplotlib rcParams using Schwab Brand style guidelines(Jumpword: Brand)
and add additional styling functions that are used for individual plot types.

The module follows the form of the seaborn styling configuration in seaborn.rcmod
for rcParams declaration and is followed by the plot specific styling functions
"""
import matplotlib.pyplot as plt


# Pallete based on Schwab Brand information design color guidelines. 
# Sequence order:
#   01) Core Blue, 02) Dark Gray, 03) Burnt Orange, 04) True Blue, 05) Turquoise,
#   06) Tangerine, 07) Cayenne, 08) Pale Blue, 09) Purple, 10) Olive Green,
#   11) Capri Blue, 12) Leaf Green, 13) Digital Core Blue, 14) Schwab Bank Dark Gray,
#   15) Jade Green, 16) Steel Blue, 17) Dark Blue 18) Orange
SCHWAB_PALETTE_HEX = [
    "#00A0DF", "#425563", "#B95E04", "#446CA9", "#64CCC9", "#FFC64D", "#C86C61",
    "#BBDDE6", "#9E4877", "#9DAE88", "#4EC1E0", "#7A9C49", "#037DAE", "#646464",
    "#127D6D", "#6BA4B8", "#02375A", "#F7A800"]
SCHWAB_PALETTE_RGB = [
    (0, 160, 223), (68, 85, 99), (185, 94, 4), (68, 108, 169), (100, 204, 201),
    (255, 198, 77), (200, 108, 97), (187, 221, 230), (158, 72, 119), (157, 174, 136),
    (78, 193, 224), (122, 156, 73), (3, 125, 174), (100, 100, 100), (18, 125, 109), 
    (107, 164, 184), (2, 55, 90), (247, 168, 0)]


def rgb_scaled(rgb_list):
    """Scales a list of RGB tuples with 0-255 RGB values to the [0, 1] interval.
    
    matplotlib only accepts RGB float values scaled on a [0, 1] interval. This 
    is accomplished by dividing tuple (R, G, B) values by the 255 max value.

    Returns:
        list: tuples (R, G, B) values scaled [0, 1].
    """
    rgb_scaled = []
    for t in rgb_list:
        r, g, b = t
        rgb_scaled.append((r / 255, g / 255, b / 255))
    return rgb_scaled


def scaled_palette():
    """
    Returns list of RGB tuples with interval [0, 1] for Schwab Brand colors
    in the order suggested in the information design palette
    """
    return rgb_scaled(SCHWAB_PALETTE_RGB)


def schwab_axes_style(style="white"):
    """
    Get the parameters that control the general style of the plots. The style
    parameters control properties like the color of the background and whether
    a grid is enabled by default. This is accomplished using the matplotlib
    rcParams system.

    This function follows the form of the seaborn.rcmod.axes_style() function.

    Args:
        style (str): one of <white|dark|whitegrid|darkgrid|ticks>
    
    Returns:
        dict: dictionary of matplotlib rcParams
    """
    styles = ["white", "dark", "whitegrid", "darkgrid", "ticks", "shadow"]
    if style not in styles:
        raise ValueError("style must be one of %s" % ", ".join(styles))

    # Define colors here
    dark_gray = "#425563"
    light_gray = "#D9D9D9"

    # Common parameters
    style_dict = {
        "figure.facecolor": "white",
        "axes.labelcolor": dark_gray,

        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.color": dark_gray,
        "ytick.color": dark_gray,

        "axes.axisbelow": True,
        "grid.linestyle": "-",

        "text.color": dark_gray,
        "font.family": ["sans-serif"],
        "font.sans-serif": [
            "Charles Modern", "Arial", "DejaVu Sans", "Liberation Sans",
            "Bitstream Vera Sans", "sans-serif"],

        "lines.solid_capstyle": "round",
        "patch.edgecolor": "w",
        "patch.force_edgecolor": True,

        "image.cmap": "rocket",

        "xtick.top": False,
        "ytick.right": False}

    # Set grid on or off
    if "grid" in style:
        style_dict.update({"axes.grid": True})
    else:
        style_dict.update({"axes.grid": False})

    # Set the color of the background, spines, and grids
    if style.startswith("dark"):
        style_dict.update({
            "axes.facecolor": "#EAEAF2",
            "axes.edgecolor": "white",
            "grid.color": "white",

            "axes.spines.left": True,
            "axes.spines.bottom": True,
            "axes.spines.right": True,
            "axes.spines.top": True})

    elif style == "whitegrid":
        style_dict.update({
            "axes.facecolor": "white",
            "axes.edgecolor": light_gray,
            "grid.color": light_gray,

            "axes.spines.left": True,
            "axes.spines.bottom": True,
            "axes.spines.right": True,
            "axes.spines.top": True})

    elif style in ["white", "ticks"]:
        style_dict.update({
            "axes.facecolor": "white",
            "axes.edgecolor": dark_gray,
            "grid.color": light_gray,

            "axes.spines.left": True,
            "axes.spines.bottom": True,
            "axes.spines.right": True,
            "axes.spines.top": True})

    elif style == "shadow":
        style_dict.update({
            #"figure.facecolor": "#F2F2F2",
            "axes.facecolor": "white",
            "axes.edgecolor": light_gray,
            "axes.grid": True,
            "grid.color": light_gray,

            "axes.spines.left": False,
            "axes.spines.bottom": False,
            "axes.spines.right": False,
            "axes.spines.top": False})

    # Show or hide the axes ticks
    if style == "ticks":
        style_dict.update({
            "xtick.bottom": True,
            "ytick.left": True})
    else:
        style_dict.update({
            "xtick.bottom": False,
            "ytick.left": False})

    return style_dict


# def schwab_context():
#     # Set up dictionary of default parameters
#     texts_base_context = {
#         "font.size": 12,
#         "axes.labelsize": 12,
#         "axes.titlesize": 12,
#         "xtick.labelsize": 11,
#         "ytick.labelsize": 11,
#         "legend.fontsize": 11,
#         "legend.title_fontsize": 12}

#     base_context = {
#         "axes.linewidth": 1.25,
#         "grid.linewidth": 1,
#         "lines.linewidth": 1.5,
#         "lines.markersize": 6,
#         "patch.linewidth": 0,

#         "xtick.major.width": 1.25,
#         "ytick.major.width": 1.25,
#         "xtick.minor.width": 1,
#         "ytick.minor.width": 1,

#         "xtick.major.size": 6,
#         "ytick.major.size": 6,
#         "xtick.minor.size": 4,
#         "ytick.minor.size": 4}


def abbreviate_tick_values(tick_val):
    """
    Reformats large tick values (in the billions, millions and thousands) such
    as 4500 into 4.5k and also appropriately turns 4000 into 4k (no zero after
    the decimal).
    """
    if tick_val >= 1_000_000_000:
        val = round(tick_val / 1_000_000_000, 1)
        new_tick_format = '{:}B'.format(val)
    elif tick_val >= 1_000_000:
        val = round(tick_val / 1_000_000, 1)
        new_tick_format = '{:}M'.format(val)
    elif tick_val >= 1_000:
        val = round(tick_val / 1_000, 1)
        new_tick_format = '{:}k'.format(val)
    elif tick_val < 1_000:
        new_tick_format = round(tick_val, 1)
    else:
        new_tick_format = tick_val

    new_tick_format = str(new_tick_format)
    index_of_decimal = new_tick_format.find(".")
    
    if index_of_decimal != -1:
        value_after_decimal = new_tick_format[index_of_decimal+1]
        if value_after_decimal == "0":
            # remove the 0 after the decimal point since it's not needed
            new_tick_format = new_tick_format[0:index_of_decimal] + new_tick_format[index_of_decimal+2:]
            
    return new_tick_format


def rotate30_xaxis(ax=None):
    """
    Rotate xaxis labels by rotating labels 30 degrees and re-anchor labels for
    better alignment. This is useful for styling charts with many ticks spread
    across the x-axis.

    Args:
        ax (obj): matplotlib.axes.Axes object.
    """
    ax = plt.gca() if ax is None else ax
    plt.setp(
        ax.xaxis.get_majorticklabels(), rotation=-30,
        ha="left", rotation_mode="anchor")

 
def thin_spine_style(side="bottom", ax=None, color="#98A4AE"):
    """Set minimal light gray line style for spine.
    
    Args:
        side (str): <left|right|bottom|top> side of axes to format spine of.
        ax (obj): matplotlib.axes.Axes object.
    """
    ax = plt.gca() if ax is None else ax
    spine = ax.spines[side]
    spine.set_visible(True)
    spine.set_color(color)
    spine.set_linewidth(0.5)
    

def line_grid(ax=None):
    """
    Set gridline and ticks for line plot using FiveThirtyEight inspired styling.

    Args:
        ax (obj): matplotlib.axes.Axes object.
    """
    pass
    

    
def tight_tick_params(ax=None):
    """
    Set tick parameter style for x and y axes to make labels smaller, bring
    them closer to the axis, and remove tick marks

    Args:
        ax (obj): matplotlib.axes.Axes object.
    """
    ax = plt.gca() if ax is None else ax
    ax.tick_params(
        axis="both", pad=-4, labelsize=7,
        bottom=False, top=False, left=False, right=False)


