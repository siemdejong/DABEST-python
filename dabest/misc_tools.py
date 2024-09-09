# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/API/misc_tools.ipynb.

# %% auto 0
__all__ = ['merge_two_dicts', 'unpack_and_add', 'print_greeting', 'get_varname', 'get_params', 'get_kwargs', 'get_color_palette',
           'initialize_fig']

# %% ../nbs/API/misc_tools.ipynb 4
import datetime as dt
import numpy as np
from numpy import repeat
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %% ../nbs/API/misc_tools.ipynb 5
def merge_two_dicts(
    x: dict, y: dict
) -> dict:  # A dictionary containing a union of all keys in both original dicts.
    """
    Given two dicts, merge them into a new dict as a shallow copy.
    Any overlapping keys in `y` will override the values in `x`.

    Taken from [here](https://stackoverflow.com/questions/38987/
    how-to-merge-two-python-dictionaries-in-a-single-expression)

    """
    z = x.copy()
    z.update(y)
    return z


def unpack_and_add(l, c):
    """Convenience function to allow me to add to an existing list
    without altering that list."""
    t = [a for a in l]
    t.append(c)
    return t


def print_greeting():
    """
    Generates a greeting message based on the current time, along with the version information of DABEST.

    This function dynamically generates a greeting ('Good morning', 'Good afternoon', 'Good evening')
    based on the current system time. It also retrieves and displays the version of DABEST (Data Analysis
    using Bootstrap-Coupled ESTimation). The message includes a header with the DABEST version and the
    current time formatted in a user-friendly manner.

    Returns:
    str: A formatted string containing the greeting message, DABEST version, and current time.
    """
    from .__init__ import __version__

    line1 = "DABEST v{}".format(__version__)
    header = "".join(repeat("=", len(line1)))
    spacer = "".join(repeat(" ", len(line1)))

    now = dt.datetime.now()
    if 0 < now.hour < 12:
        greeting = "Good morning!"
    elif 12 < now.hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"

    current_time = "The current time is {}.".format(now.ctime())

    return "\n".join([line1, header, spacer, greeting, current_time])


def get_varname(obj):
    matching_vars = [k for k, v in globals().items() if v is obj]
    if len(matching_vars) > 0:
        return matching_vars[0]
    return ""

def get_params(effectsize_df, plot_kwargs):
    """
    Parameters
    ----------
    effectsize_df : object (Dataframe)
        A `dabest` EffectSizeDataFrame object.
    plot_kwargs : dict
        Kwargs passed to the plot function.
    """
    face_color = plot_kwargs["face_color"]

    if plot_kwargs["face_color"] is None:
        face_color = "white"

    dabest_obj = effectsize_df.dabest_obj
    plot_data = effectsize_df._plot_data
    xvar = effectsize_df.xvar
    yvar = effectsize_df.yvar
    is_paired = effectsize_df.is_paired
    delta2 = effectsize_df.delta2
    mini_meta = effectsize_df.mini_meta
    effect_size = effectsize_df.effect_size
    proportional = effectsize_df.proportional

    all_plot_groups = dabest_obj._all_plot_groups
    idx = dabest_obj.idx

    if effect_size not in ["mean_diff", "delta_g"] or not delta2:
        show_delta2 = False
    else:
        show_delta2 = plot_kwargs["show_delta2"]

    if effect_size != "mean_diff" or not mini_meta:
        show_mini_meta = False
    else:
        show_mini_meta = plot_kwargs["show_mini_meta"]

    if show_delta2 and show_mini_meta: raise ValueError("`show_delta2` and `show_mini_meta` cannot be True at the same time.")

    # Disable Gardner-Altman plotting if any of the idxs comprise of more than
    # two groups or if it is a delta-delta plot.
    float_contrast = plot_kwargs["float_contrast"]
    effect_size_type = effectsize_df.effect_size
    if len(idx) > 1 or len(idx[0]) > 2:
        float_contrast = False

    if effect_size_type in ["cliffs_delta"]:
        float_contrast = False

    if show_delta2 or show_mini_meta:
        float_contrast = False

    if not is_paired:
        show_pairs = False
    else:
        show_pairs = plot_kwargs["show_pairs"]

    # Group summaries
    group_summaries = plot_kwargs["group_summaries"]
    if group_summaries is None:
        group_summaries = "mean_sd"

    # Error bar color
    err_color = plot_kwargs["err_color"]
    if err_color is None: 
        err_color = "black"
        

    return (face_color, dabest_obj, plot_data, xvar, yvar, is_paired, effect_size, proportional, all_plot_groups, idx, 
            show_delta2, show_mini_meta, float_contrast, show_pairs, effect_size_type, group_summaries, err_color)

def get_kwargs(plot_kwargs, ytick_color):
    """
    Parameters
    ----------
    plot_kwargs : dict
        Kwargs passed to the plot function.
    ytick_color : str
        Color of the yticks.
    """
    from .misc_tools import merge_two_dicts

    # Swarmplot kwargs
    default_swarmplot_kwargs = {"size": plot_kwargs["raw_marker_size"]}
    if plot_kwargs["swarmplot_kwargs"] is None:
        swarmplot_kwargs = default_swarmplot_kwargs
    else:
        swarmplot_kwargs = merge_two_dicts(
            default_swarmplot_kwargs, plot_kwargs["swarmplot_kwargs"]
        )

    # Barplot kwargs
    default_barplot_kwargs = {"estimator": np.mean, "errorbar": plot_kwargs["ci"]}
    if plot_kwargs["barplot_kwargs"] is None:
        barplot_kwargs = default_barplot_kwargs
    else:
        barplot_kwargs = merge_two_dicts(
            default_barplot_kwargs, plot_kwargs["barplot_kwargs"]
        )

    # Sankey Diagram kwargs
    default_sankey_kwargs = {
        "width": 0.4,
        "align": "center",
        "sankey": True,
        "flow": True,
        "alpha": 0.4,
        "rightColor": False,
        "bar_width": 0.2,
    }
    if plot_kwargs["sankey_kwargs"] is None:
        sankey_kwargs = default_sankey_kwargs
    else:
        sankey_kwargs = merge_two_dicts(
            default_sankey_kwargs, plot_kwargs["sankey_kwargs"]
        )

    # Violinplot kwargs.
    default_violinplot_kwargs = {
        "widths": 0.5,
        "vert": True,
        "showextrema": False,
        "showmedians": False,
    }
    if plot_kwargs["violinplot_kwargs"] is None:
        violinplot_kwargs = default_violinplot_kwargs
    else:
        violinplot_kwargs = merge_two_dicts(
            default_violinplot_kwargs, plot_kwargs["violinplot_kwargs"]
        )

    # Slopegraph kwargs.
    default_slopegraph_kwargs = {"linewidth": 1, "alpha": 0.5}
    if plot_kwargs["slopegraph_kwargs"] is None:
        slopegraph_kwargs = default_slopegraph_kwargs
    else:
        slopegraph_kwargs = merge_two_dicts(
            default_slopegraph_kwargs, plot_kwargs["slopegraph_kwargs"]
        )

    # Zero reference-line kwargs.
    default_reflines_kwargs = {
        "linestyle": "solid",
        "linewidth": 0.75,
        "zorder": 2,
        "color": ytick_color,
    }
    if plot_kwargs["reflines_kwargs"] is None:
        reflines_kwargs = default_reflines_kwargs
    else:
        reflines_kwargs = merge_two_dicts(
            default_reflines_kwargs, plot_kwargs["reflines_kwargs"]
        )

    # Legend kwargs.
    default_legend_kwargs = {"loc": "upper left", "frameon": False}
    if plot_kwargs["legend_kwargs"] is None:
        legend_kwargs = default_legend_kwargs
    else:
        legend_kwargs = merge_two_dicts(
            default_legend_kwargs, plot_kwargs["legend_kwargs"]
        )

    # Group summaries kwargs.
    gs_default = {"mean_sd", "median_quartiles", None}
    if plot_kwargs["group_summaries"] not in gs_default:
        raise ValueError(
            "group_summaries must be one of" " these: {}.".format(gs_default)
        )

    default_group_summary_kwargs = {"zorder": 3, "lw": 2, "alpha": 1}
    if plot_kwargs["group_summary_kwargs"] is None:
        group_summary_kwargs = default_group_summary_kwargs
    else:
        group_summary_kwargs = merge_two_dicts(
            default_group_summary_kwargs, plot_kwargs["group_summary_kwargs"]
        )

    # Redraw axes kwargs.
    redraw_axes_kwargs = {
        "colors": ytick_color,
        "facecolors": ytick_color,
        "lw": 1,
        "zorder": 10,
        "clip_on": False,
    }
    
    # Delta dots kwargs.
    default_delta_dot_kwargs = {"marker": "^", "alpha": 0.5, "zorder": 2, "size": 3, "side": "right"}
    if plot_kwargs["delta_dot_kwargs"] is None:
        delta_dot_kwargs = default_delta_dot_kwargs
    else:
        delta_dot_kwargs = merge_two_dicts(default_delta_dot_kwargs, plot_kwargs["delta_dot_kwargs"])

    # Delta text kwargs.
    default_delta_text_kwargs = {"color": None, "alpha": 1, "fontsize": 10, "ha": 'center', "va": 'center', "rotation": 0, "x_location": 'right', "x_coordinates": None, "y_coordinates": None}
    if plot_kwargs["delta_text_kwargs"] is None:
        delta_text_kwargs = default_delta_text_kwargs
    else:
        delta_text_kwargs = merge_two_dicts(default_delta_text_kwargs, plot_kwargs["delta_text_kwargs"])

    # Summary bars kwargs.
    default_summary_bars_kwargs = {"color": None, "alpha": 0.15}
    if plot_kwargs["summary_bars_kwargs"] is None:
        summary_bars_kwargs = default_summary_bars_kwargs
    else:
        summary_bars_kwargs = merge_two_dicts(default_summary_bars_kwargs, plot_kwargs["summary_bars_kwargs"])

    # Swarm bars kwargs.
    default_swarm_bars_kwargs = {"color": None, "alpha": 0.3}
    if plot_kwargs["swarm_bars_kwargs"] is None:
        swarm_bars_kwargs = default_swarm_bars_kwargs
    else:
        swarm_bars_kwargs = merge_two_dicts(default_swarm_bars_kwargs, plot_kwargs["swarm_bars_kwargs"])

    # Contrast bars kwargs.
    default_contrast_bars_kwargs = {"color": None, "alpha": 0.3}
    if plot_kwargs["contrast_bars_kwargs"] is None:
        contrast_bars_kwargs = default_contrast_bars_kwargs
    else:
        contrast_bars_kwargs = merge_two_dicts(default_contrast_bars_kwargs, plot_kwargs["contrast_bars_kwargs"])

    return (swarmplot_kwargs, barplot_kwargs, sankey_kwargs, violinplot_kwargs, slopegraph_kwargs, 
            reflines_kwargs, legend_kwargs, group_summary_kwargs, redraw_axes_kwargs, delta_dot_kwargs,
            delta_text_kwargs, summary_bars_kwargs, swarm_bars_kwargs, contrast_bars_kwargs)


def get_color_palette(plot_kwargs, plot_data, xvar, show_pairs):

    # Create color palette that will be shared across subplots.
    color_col = plot_kwargs["color_col"]
    if color_col is None:
        color_groups = pd.unique(plot_data[xvar])
        bootstraps_color_by_group = True
    else:
        if color_col not in plot_data.columns:
            raise KeyError("``{}`` is not a column in the data.".format(color_col))
        color_groups = pd.unique(plot_data[color_col])
        bootstraps_color_by_group = False
    if show_pairs:
        bootstraps_color_by_group = False

    # Handle the color palette.
    names = color_groups
    n_groups = len(color_groups)
    custom_pal = plot_kwargs["custom_palette"]
    swarm_desat = plot_kwargs["swarm_desat"]
    bar_desat = plot_kwargs["bar_desat"]
    contrast_desat = plot_kwargs["halfviolin_desat"]

    if custom_pal is None:
        unsat_colors = sns.color_palette(n_colors=n_groups)
    else:
        if isinstance(custom_pal, dict):
            groups_in_palette = {
                k: v for k, v in custom_pal.items() if k in color_groups
            }

            names = groups_in_palette.keys()
            unsat_colors = groups_in_palette.values()

        elif isinstance(custom_pal, list):
            unsat_colors = custom_pal[0:n_groups]

        elif isinstance(custom_pal, str):
            # check it is in the list of matplotlib palettes.
            if custom_pal in plt.colormaps():
                unsat_colors = sns.color_palette(custom_pal, n_groups)
            else:
                err1 = "The specified `custom_palette` {}".format(custom_pal)
                err2 = " is not a matplotlib palette. Please check."
                raise ValueError(err1 + err2)
            

    if custom_pal is None and color_col is None:
        swarm_colors = [sns.desaturate(c, swarm_desat) for c in unsat_colors]
        plot_palette_raw = dict(zip(names.categories, swarm_colors))

        bar_color = [sns.desaturate(c, bar_desat) for c in unsat_colors]
        plot_palette_bar = dict(zip(names.categories, bar_color))

        contrast_colors = [sns.desaturate(c, contrast_desat) for c in unsat_colors]
        plot_palette_contrast = dict(zip(names.categories, contrast_colors))

        # For Sankey Diagram plot, no need to worry about the color, each bar will have the same two colors
        # default color palette will be set to "hls"
        plot_palette_sankey = None

    else:
        swarm_colors = [sns.desaturate(c, swarm_desat) for c in unsat_colors]
        plot_palette_raw = dict(zip(names, swarm_colors))

        bar_color = [sns.desaturate(c, bar_desat) for c in unsat_colors]
        plot_palette_bar = dict(zip(names, bar_color))

        contrast_colors = [sns.desaturate(c, contrast_desat) for c in unsat_colors]
        plot_palette_contrast = dict(zip(names, contrast_colors))

        plot_palette_sankey = custom_pal

    return (color_col, bootstraps_color_by_group, n_groups, swarm_colors, plot_palette_raw, 
            bar_color, plot_palette_bar, plot_palette_contrast, plot_palette_sankey)

def initialize_fig(plot_kwargs, dabest_obj, show_delta2, show_mini_meta, is_paired, show_pairs, proportional,
                   float_contrast, face_color, h_space_cummings):
    fig_size = plot_kwargs["fig_size"]
    if fig_size is None:
        all_groups_count = np.sum([len(i) for i in dabest_obj.idx])
        # Increase the width for delta-delta graph
        if show_delta2 or show_mini_meta:
            all_groups_count += 2
        if is_paired and show_pairs and proportional is False:
            frac = 0.75
        else:
            frac = 1
        if float_contrast:
            height_inches = 4
            each_group_width_inches = 2.5 * frac
        else:
            height_inches = 6
            each_group_width_inches = 1.5 * frac

        width_inches = each_group_width_inches * all_groups_count
        fig_size = (width_inches, height_inches)

    init_fig_kwargs = dict(figsize=fig_size, dpi=plot_kwargs["dpi"], tight_layout=True)
    width_ratios_ga = [2.5, 1]

    if plot_kwargs["ax"] is not None:
        # New in v0.2.6.
        # Use inset axes to create the estimation plot inside a single axes.
        # Author: Adam L Nekimken. (PR #73)
        rawdata_axes = plot_kwargs["ax"]
        ax_position = rawdata_axes.get_position()  # [[x0, y0], [x1, y1]]

        fig = rawdata_axes.get_figure()
        fig.patch.set_facecolor(face_color)

        if float_contrast:
            axins = rawdata_axes.inset_axes(
                [1, 0, width_ratios_ga[1] / width_ratios_ga[0], 1]
            )
            rawdata_axes.set_position(  # [l, b, w, h]
                [
                    ax_position.x0,
                    ax_position.y0,
                    (ax_position.x1 - ax_position.x0)
                    * (width_ratios_ga[0] / sum(width_ratios_ga)),
                    (ax_position.y1 - ax_position.y0),
                ]
            )

            contrast_axes = axins
        else:
            axins = rawdata_axes.inset_axes([0, -1 - h_space_cummings, 1, 1])
            plot_height = (ax_position.y1 - ax_position.y0) / (2 + h_space_cummings)
            rawdata_axes.set_position(
                [
                    ax_position.x0,
                    ax_position.y0 + (1 + h_space_cummings) * plot_height,
                    (ax_position.x1 - ax_position.x0),
                    plot_height,
                ]
            )

        contrast_axes = axins
        rawdata_axes.contrast_axes = axins

    else:
        # Here, we hardcode some figure parameters.
        if float_contrast:
            fig, axx = plt.subplots(
                ncols=2,
                gridspec_kw={"width_ratios": width_ratios_ga, "wspace": 0},
                **init_fig_kwargs
            )
            fig.patch.set_facecolor(face_color)

        else:
            fig, axx = plt.subplots(
                nrows=2, gridspec_kw={"hspace": h_space_cummings}, **init_fig_kwargs
            )
            fig.patch.set_facecolor(face_color)

        # Title
        title = plot_kwargs["title"]
        fontsize_title = plot_kwargs["fontsize_title"]
        if title is not None:
            fig.suptitle(title, fontsize=fontsize_title)
        rawdata_axes = axx[0]
        contrast_axes = axx[1]
    rawdata_axes.set_frame_on(False)
    contrast_axes.set_frame_on(False)

    swarm_ylim = plot_kwargs["swarm_ylim"]
    if swarm_ylim is not None:
        rawdata_axes.set_ylim(swarm_ylim)

    return fig, rawdata_axes, contrast_axes, swarm_ylim
