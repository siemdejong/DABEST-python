# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/API/misc_tools.ipynb.

# %% auto 0
__all__ = ['merge_two_dicts', 'unpack_and_add', 'print_greeting', 'get_varname', 'get_params', 'get_kwargs', 'get_color_palette',
           'initialize_fig', 'get_plot_groups', 'add_counts_to_ticks', 'extract_contrast_plotting_ticks',
           'set_xaxis_ticks_and_lims', 'show_legend', 'Gardner_Altman_Plot_Aesthetic_Adjustments',
           'Cumming_Plot_Aesthetic_Adjustments', 'General_Plot_Aesthetic_Adjustments']

# %% ../nbs/API/misc_tools.ipynb 4
import datetime as dt
import numpy as np
from numpy import repeat
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

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
        
    return (dabest_obj, plot_data, xvar, yvar, is_paired, effect_size, proportional, all_plot_groups, idx, 
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
                   float_contrast):
    # Params
    fig_size = plot_kwargs["fig_size"]
    face_color = plot_kwargs["face_color"]
    if plot_kwargs["face_color"] is None:
        face_color = "white"

    if fig_size is None:
        all_groups_count = np.sum([len(i) for i in dabest_obj.idx])
        # Increase the width for delta-delta graph
        if show_delta2 or show_mini_meta:
            all_groups_count += 2
        if is_paired and show_pairs and proportional is False:
            frac = 0.8
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

    h_space_cummings = 0.3 if plot_kwargs["gridkey_rows"] == None else 0.1     ##### GRIDKEY WIP addition

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

def get_plot_groups(is_paired, idx, proportional, all_plot_groups):

    if is_paired == "baseline":
        idx_pairs = [
            (control, test)
            for i in idx
            for control, test in zip([i[0]] * (len(i) - 1), i[1:])
        ]
        temp_idx = idx if not proportional else idx_pairs
    else:
        idx_pairs = [
            (control, test) for i in idx for control, test in zip(i[:-1], i[1:])
        ]
        temp_idx = idx if not proportional else idx_pairs

    # Determine temp_all_plot_groups based on proportional condition
    plot_groups = [item for i in temp_idx for item in i]
    temp_all_plot_groups = all_plot_groups if not proportional else plot_groups
    
    return temp_idx, temp_all_plot_groups


def add_counts_to_ticks(plot_data, xvar, yvar, rawdata_axes, plot_kwargs):
    counts = plot_data.groupby(xvar).count()[yvar]
    ticks_with_counts = []
    ticks_loc = rawdata_axes.get_xticks()
    rawdata_axes.xaxis.set_major_locator(matplotlib.ticker.FixedLocator(ticks_loc))
    for xticklab in rawdata_axes.xaxis.get_ticklabels():
        t = xticklab.get_text()
        if t.rfind("\n") != -1:
            te = t[t.rfind("\n") + len("\n") :]
            N = str(counts.loc[te])
            te = t
        else:
            te = t
            N = str(counts.loc[te])

        ticks_with_counts.append("{}\nN = {}".format(te, N))

    if plot_kwargs["fontsize_rawxlabel"] is not None:
        fontsize_rawxlabel = plot_kwargs["fontsize_rawxlabel"]
    rawdata_axes.set_xticklabels(ticks_with_counts, fontsize=fontsize_rawxlabel)


def extract_contrast_plotting_ticks(is_paired, show_pairs, two_col_sankey, plot_groups, idx, sankey_control_group):

    # Take note of where the `control` groups are.
    ticks_to_skip_contrast = None
    ticks_to_start_twocol_sankey = None
    if is_paired == "baseline" and show_pairs:
        if two_col_sankey:
            ticks_to_skip = []
            ticks_to_plot = np.arange(0, len(plot_groups) / 2).tolist()
            ticks_to_start_twocol_sankey = np.cumsum([len(i) - 1 for i in idx]).tolist()
            ticks_to_start_twocol_sankey.pop()
            ticks_to_start_twocol_sankey.insert(0, 0)
        else:
            # ticks_to_skip = np.arange(0, len(temp_all_plot_groups), 2).tolist()
            # ticks_to_plot = np.arange(1, len(temp_all_plot_groups), 2).tolist()
            ticks_to_skip = np.cumsum([len(t) for t in idx])[:-1].tolist()
            ticks_to_skip.insert(0, 0)
            # Then obtain the ticks where we have to plot the effect sizes.
            ticks_to_plot = [
                t for t in range(0, len(plot_groups)) if t not in ticks_to_skip
            ]
            ticks_to_skip_contrast = np.cumsum([(len(t)) for t in idx])[:-1].tolist()
            ticks_to_skip_contrast.insert(0, 0)
    else:
        if two_col_sankey:
            ticks_to_skip = [len(sankey_control_group)]
            # Then obtain the ticks where we have to plot the effect sizes.
            ticks_to_plot = [
                t for t in range(0, len(plot_groups)) if t not in ticks_to_skip
            ]
            ticks_to_skip = []
            ticks_to_start_twocol_sankey = np.cumsum([len(i) - 1 for i in idx]).tolist()
            ticks_to_start_twocol_sankey.pop()
            ticks_to_start_twocol_sankey.insert(0, 0)
        else:
            ticks_to_skip = np.cumsum([len(t) for t in idx])[:-1].tolist()
            ticks_to_skip.insert(0, 0)
            # Then obtain the ticks where we have to plot the effect sizes.
            ticks_to_plot = [
                t for t in range(0, len(plot_groups)) if t not in ticks_to_skip
            ]
    
    return ticks_to_skip, ticks_to_plot, ticks_to_skip_contrast, ticks_to_start_twocol_sankey

def set_xaxis_ticks_and_lims(show_delta2, show_mini_meta, rawdata_axes, contrast_axes, show_pairs, float_contrast,
                             ticks_to_skip, contrast_xtick_labels, plot_kwargs):

    if show_delta2 is False and show_mini_meta is False:
        contrast_axes.set_xticks(rawdata_axes.get_xticks())
    else:
        temp = rawdata_axes.get_xticks()
        temp = np.append(temp, [max(temp) + 1, max(temp) + 2])
        contrast_axes.set_xticks(temp)

    if show_pairs:
        max_x = contrast_axes.get_xlim()[1]
        rawdata_axes.set_xlim(-0.375, max_x)

    if float_contrast:
        contrast_axes.set_xlim(0.5, 1.5)
    elif show_delta2 or show_mini_meta:
        # Increase the xlim of raw data by 2
        temp = rawdata_axes.get_xlim()
        if show_pairs:
            rawdata_axes.set_xlim(temp[0], temp[1] + 0.25)
        else:
            rawdata_axes.set_xlim(temp[0], temp[1] + 2)
        contrast_axes.set_xlim(rawdata_axes.get_xlim())
    else:
        contrast_axes.set_xlim(rawdata_axes.get_xlim())

    # Properly label the contrast ticks.
    for t in ticks_to_skip:
        contrast_xtick_labels.insert(t, "")

    if plot_kwargs["fontsize_contrastxlabel"] is not None:
        fontsize_contrastxlabel = plot_kwargs["fontsize_contrastxlabel"]

    contrast_axes.set_xticklabels(
        contrast_xtick_labels, fontsize=fontsize_contrastxlabel
    )


def show_legend(legend_labels, legend_handles, rawdata_axes, contrast_axes, float_contrast, show_pairs, legend_kwargs):

    legend_labels_unique = np.unique(legend_labels)
    unique_idx = np.unique(legend_labels, return_index=True)[1]
    legend_handles_unique = (
        pd.Series(legend_handles, dtype="object").loc[unique_idx]
    ).tolist()

    if len(legend_handles_unique) > 0:
        if float_contrast:
            axes_with_legend = contrast_axes
            if show_pairs:
                bta = (2.00, 1.02)
            else:
                bta = (1.5, 1.02)
        else:
            axes_with_legend = rawdata_axes
            if show_pairs:
                bta = (1.02, 1.0)
            else:
                bta = (1.0, 1.0)
        leg = axes_with_legend.legend(
            legend_handles_unique,
            legend_labels_unique,
            bbox_to_anchor=bta,
            **legend_kwargs
        )
        if show_pairs:
            for line in leg.get_lines():
                line.set_linewidth(3.0)
    
def Gardner_Altman_Plot_Aesthetic_Adjustments(effect_size_type, plot_data, xvar, yvar, current_control, current_group,
                                         rawdata_axes, contrast_axes, results, current_effsize, is_paired, one_sankey,
                                         reflines_kwargs, redraw_axes_kwargs, swarm_ylim, og_xlim_raw, og_ylim_raw):
    from ._stats_tools.effsize import (
        _compute_standardizers,
        _compute_hedges_correction_factor,
    )
    # Normalize ylims and despine the floating contrast axes.
    # Check that the effect size is within the swarm ylims.
    if effect_size_type in ["mean_diff", "cohens_d", "hedges_g", "cohens_h"]:
        control_group_summary = (
            plot_data.groupby(xvar)
            .mean(numeric_only=True)
            .loc[current_control, yvar]
        )
        test_group_summary = (
            plot_data.groupby(xvar).mean(numeric_only=True).loc[current_group, yvar]
        )
    elif effect_size_type == "median_diff":
        control_group_summary = (
            plot_data.groupby(xvar).median().loc[current_control, yvar]
        )
        test_group_summary = (
            plot_data.groupby(xvar).median().loc[current_group, yvar]
        )

    if swarm_ylim is None:
        swarm_ylim = rawdata_axes.get_ylim()

    _, contrast_xlim_max = contrast_axes.get_xlim()

    difference = float(results.difference[0])

    if effect_size_type in ["mean_diff", "median_diff"]:
        # Align 0 of contrast_axes to reference group mean of rawdata_axes.
        # If the effect size is positive, shift the contrast axis up.
        rawdata_ylims = np.array(rawdata_axes.get_ylim())
        if current_effsize > 0:
            rightmin, rightmax = rawdata_ylims - current_effsize
        # If the effect size is negative, shift the contrast axis down.
        elif current_effsize < 0:
            rightmin, rightmax = rawdata_ylims + current_effsize
        else:
            rightmin, rightmax = rawdata_ylims

        contrast_axes.set_ylim(rightmin, rightmax)

        og_ylim_contrast = rawdata_axes.get_ylim() - np.array(control_group_summary)

        contrast_axes.set_ylim(og_ylim_contrast)
        contrast_axes.set_xlim(contrast_xlim_max - 1, contrast_xlim_max)

    elif effect_size_type in ["cohens_d", "hedges_g", "cohens_h"]:
        if is_paired:
            which_std = 1
        else:
            which_std = 0
        temp_control = plot_data[plot_data[xvar] == current_control][yvar]
        temp_test = plot_data[plot_data[xvar] == current_group][yvar]

        stds = _compute_standardizers(temp_control, temp_test)
        if is_paired:
            pooled_sd = stds[1]
        else:
            pooled_sd = stds[0]

        if effect_size_type == "hedges_g":
            gby_count = plot_data.groupby(xvar).count()
            len_control = gby_count.loc[current_control, yvar]
            len_test = gby_count.loc[current_group, yvar]

            hg_correction_factor = _compute_hedges_correction_factor(
                len_control, len_test
            )

            ylim_scale_factor = pooled_sd / hg_correction_factor

        elif effect_size_type == "cohens_h":
            ylim_scale_factor = (
                np.mean(temp_test) - np.mean(temp_control)
            ) / difference

        else:
            ylim_scale_factor = pooled_sd

        scaled_ylim = (
            (rawdata_axes.get_ylim() - control_group_summary) / ylim_scale_factor
        ).tolist()

        contrast_axes.set_ylim(scaled_ylim)
        og_ylim_contrast = scaled_ylim

        contrast_axes.set_xlim(contrast_xlim_max - 1, contrast_xlim_max)

    if one_sankey is None:
        # Draw summary lines for control and test groups..
        for jj, axx in enumerate([rawdata_axes, contrast_axes]):
            # Draw effect size line.
            if jj == 0:
                ref = control_group_summary
                diff = test_group_summary
                effsize_line_start = 1

            elif jj == 1:
                ref = 0
                diff = ref + difference
                effsize_line_start = contrast_xlim_max - 1.1

            xlimlow, xlimhigh = axx.get_xlim()

            # Draw reference line.
            axx.hlines(
                ref,  # y-coordinates
                0,
                xlimhigh,  # x-coordinates, start and end.
                **reflines_kwargs
            )

            # Draw effect size line.
            axx.hlines(diff, effsize_line_start, xlimhigh, **reflines_kwargs)
    else:
        ref = 0
        diff = ref + difference
        effsize_line_start = contrast_xlim_max - 0.9
        xlimlow, xlimhigh = contrast_axes.get_xlim()
        # Draw reference line.
        contrast_axes.hlines(
            ref,  # y-coordinates
            effsize_line_start,
            xlimhigh,  # x-coordinates, start and end.
            **reflines_kwargs
        )

        # Draw effect size line.
        contrast_axes.hlines(diff, effsize_line_start, xlimhigh, **reflines_kwargs)
    rawdata_axes.set_xlim(og_xlim_raw)  # to align the axis
    # Despine appropriately.
    sns.despine(ax=rawdata_axes, bottom=True)
    sns.despine(ax=contrast_axes, left=True, right=False)

    # Insert break between the rawdata axes and the contrast axes
    # by re-drawing the x-spine.
    rawdata_axes.hlines(
        og_ylim_raw[0],  # yindex
        rawdata_axes.get_xlim()[0],
        1.3,  # xmin, xmax
        **redraw_axes_kwargs
    )
    rawdata_axes.set_ylim(og_ylim_raw)

    contrast_axes.hlines(
        contrast_axes.get_ylim()[0],
        contrast_xlim_max - 0.8,
        contrast_xlim_max,
        **redraw_axes_kwargs
    )


def Cumming_Plot_Aesthetic_Adjustments(plot_kwargs, show_delta2, effect_size_type, contrast_axes, reflines_kwargs, 
                                       is_paired, show_pairs, two_col_sankey, idx, ticks_to_start_twocol_sankey,
                                       proportional, ticks_to_skip, temp_idx, rawdata_axes, redraw_axes_kwargs,
                                       ticks_to_skip_contrast):
    # Set custom contrast_ylim, if it was specified.
    if plot_kwargs["contrast_ylim"] is not None or (
        plot_kwargs["delta2_ylim"] is not None and show_delta2
    ):
        if plot_kwargs["contrast_ylim"] is not None:
            custom_contrast_ylim = plot_kwargs["contrast_ylim"]
            if plot_kwargs["delta2_ylim"] is not None and show_delta2:
                custom_delta2_ylim = plot_kwargs["delta2_ylim"]
                if custom_contrast_ylim != custom_delta2_ylim:
                    err1 = "Please check if `contrast_ylim` and `delta2_ylim` are assigned"
                    err2 = "with same values."
                    raise ValueError(err1 + err2)
        else:
            custom_delta2_ylim = plot_kwargs["delta2_ylim"]
            custom_contrast_ylim = custom_delta2_ylim

        if len(custom_contrast_ylim) != 2:
            err1 = "Please check `contrast_ylim` consists of "
            err2 = "exactly two numbers."
            raise ValueError(err1 + err2)

        if effect_size_type == "cliffs_delta":
            # Ensure the ylims for a cliffs_delta plot never exceed [-1, 1].
            l = plot_kwargs["contrast_ylim"][0]
            h = plot_kwargs["contrast_ylim"][1]
            low = -1 if l < -1 else l
            high = 1 if h > 1 else h
            contrast_axes.set_ylim(low, high)
        else:
            contrast_axes.set_ylim(custom_contrast_ylim)


    # If 0 lies within the ylim of the contrast axes,
    # draw a zero reference line.
    contrast_axes_ylim = contrast_axes.get_ylim()
    if contrast_axes_ylim[0] < contrast_axes_ylim[1]:
        contrast_ylim_low, contrast_ylim_high = contrast_axes_ylim
    else:
        contrast_ylim_high, contrast_ylim_low = contrast_axes_ylim
    if contrast_ylim_low < 0 < contrast_ylim_high:
        contrast_axes.axhline(y=0, **reflines_kwargs)

    if is_paired == "baseline" and show_pairs:
                if two_col_sankey:
                    rightend_ticks_raw = np.array([len(i) - 2 for i in idx]) + np.array(
                        ticks_to_start_twocol_sankey
                    )
                elif proportional and is_paired is not None:
                    rightend_ticks_raw = np.array([len(i) - 1 for i in idx]) + np.array(
                        ticks_to_skip
                    )
                else:
                    rightend_ticks_raw = np.array(
                        [len(i) - 1 for i in temp_idx]
                    ) + np.array(ticks_to_skip)
                for ax in [rawdata_axes]:
                    sns.despine(ax=ax, bottom=True)

                    ylim = ax.get_ylim()
                    xlim = ax.get_xlim()
                    redraw_axes_kwargs["y"] = ylim[0]

                    if two_col_sankey:
                        for k, start_tick in enumerate(ticks_to_start_twocol_sankey):
                            end_tick = rightend_ticks_raw[k]
                            ax.hlines(xmin=start_tick, xmax=end_tick, **redraw_axes_kwargs)
                    else:
                        for k, start_tick in enumerate(ticks_to_skip):
                            end_tick = rightend_ticks_raw[k]
                            ax.hlines(xmin=start_tick, xmax=end_tick, **redraw_axes_kwargs)
                    ax.set_ylim(ylim)
                    del redraw_axes_kwargs["y"]

                if not proportional:
                    temp_length = [(len(i) - 1) for i in idx]
                else:
                    temp_length = [(len(i) - 1) * 2 - 1 for i in idx]
                if two_col_sankey:
                    rightend_ticks_contrast = np.array(
                        [len(i) - 2 for i in idx]
                    ) + np.array(ticks_to_start_twocol_sankey)
                elif proportional and is_paired is not None:
                    rightend_ticks_contrast = np.array(
                        [len(i) - 1 for i in idx]
                    ) + np.array(ticks_to_skip)
                else:
                    rightend_ticks_contrast = np.array(temp_length) + np.array(
                        ticks_to_skip_contrast
                    )
                for ax in [contrast_axes]:
                    sns.despine(ax=ax, bottom=True)

                    ylim = ax.get_ylim()
                    xlim = ax.get_xlim()
                    redraw_axes_kwargs["y"] = ylim[0]

                    if two_col_sankey:
                        for k, start_tick in enumerate(ticks_to_start_twocol_sankey):
                            end_tick = rightend_ticks_contrast[k]
                            ax.hlines(xmin=start_tick, xmax=end_tick, **redraw_axes_kwargs)
                    else:
                        for k, start_tick in enumerate(ticks_to_skip_contrast):
                            end_tick = rightend_ticks_contrast[k]
                            ax.hlines(xmin=start_tick, xmax=end_tick, **redraw_axes_kwargs)

                    ax.set_ylim(ylim)
                    del redraw_axes_kwargs["y"]
    else:
        # Compute the end of each x-axes line.
        if two_col_sankey:
            rightend_ticks = np.array([len(i) - 2 for i in idx]) + np.array(
                ticks_to_start_twocol_sankey
            )
        else:
            rightend_ticks = np.array([len(i) - 1 for i in idx]) + np.array(
                ticks_to_skip
            )

        for ax in [rawdata_axes, contrast_axes]:
            sns.despine(ax=ax, bottom=True)

            ylim = ax.get_ylim()
            xlim = ax.get_xlim()
            redraw_axes_kwargs["y"] = ylim[0]

            if two_col_sankey:
                for k, start_tick in enumerate(ticks_to_start_twocol_sankey):
                    end_tick = rightend_ticks[k]
                    ax.hlines(xmin=start_tick, xmax=end_tick, **redraw_axes_kwargs)
            else:
                for k, start_tick in enumerate(ticks_to_skip):
                    end_tick = rightend_ticks[k]
                    ax.hlines(xmin=start_tick, xmax=end_tick, **redraw_axes_kwargs)

            ax.set_ylim(ylim)
            del redraw_axes_kwargs["y"]

def General_Plot_Aesthetic_Adjustments(show_delta2, show_mini_meta, contrast_axes, redraw_axes_kwargs, plot_kwargs,
                               yvar, effect_size_type, proportional, effectsize_df, is_paired, float_contrast,
                               rawdata_axes, og_ylim_raw, effect_size):

    if show_delta2 or show_mini_meta:
        ylim = contrast_axes.get_ylim()
        redraw_axes_kwargs["y"] = ylim[0]
        x_ticks = contrast_axes.get_xticks()
        contrast_axes.hlines(xmin=x_ticks[-2], xmax=x_ticks[-1], **redraw_axes_kwargs)
        del redraw_axes_kwargs["y"]

    # Set raw axes y-label.
    swarm_label = plot_kwargs["swarm_label"]
    if swarm_label is None and yvar is None:
        swarm_label = "value"
    elif swarm_label is None and yvar is not None:
        swarm_label = yvar

    bar_label = plot_kwargs["bar_label"]
    if bar_label is None and effect_size_type != "cohens_h":
        bar_label = "proportion of success"
    elif bar_label is None and effect_size_type == "cohens_h":
        bar_label = "value"

    # Place contrast axes y-label.
    contrast_label_dict = {
        "mean_diff": "mean difference",
        "median_diff": "median difference",
        "cohens_d": "Cohen's d",
        "hedges_g": "Hedges' g",
        "cliffs_delta": "Cliff's delta",
        "cohens_h": "Cohen's h",
        "delta_g": "mean difference",
    }

    if proportional and effect_size_type != "cohens_h":
        default_contrast_label = "proportion difference"
    elif effect_size_type == "delta_g":
        default_contrast_label = "Hedges' g"
    else:
        default_contrast_label = contrast_label_dict[effectsize_df.effect_size]

    if plot_kwargs["contrast_label"] is None:
        if is_paired:
            contrast_label = "paired\n{}".format(default_contrast_label)
        else:
            contrast_label = default_contrast_label
        contrast_label = contrast_label.capitalize()
    else:
        contrast_label = plot_kwargs["contrast_label"]

    if plot_kwargs["fontsize_rawylabel"] is not None:
        fontsize_rawylabel = plot_kwargs["fontsize_rawylabel"]
    if plot_kwargs["fontsize_contrastylabel"] is not None:
        fontsize_contrastylabel = plot_kwargs["fontsize_contrastylabel"]
    if plot_kwargs["fontsize_delta2label"] is not None:
        fontsize_delta2label = plot_kwargs["fontsize_delta2label"]

    contrast_axes.set_ylabel(contrast_label, fontsize=fontsize_contrastylabel)
    if float_contrast:
        contrast_axes.yaxis.set_label_position("right")

    # Set the rawdata axes labels appropriately
    if not proportional:
        rawdata_axes.set_ylabel(swarm_label, fontsize=fontsize_rawylabel)
    else:
        rawdata_axes.set_ylabel(bar_label, fontsize=fontsize_rawylabel)
    rawdata_axes.set_xlabel("")

    # Because we turned the axes frame off, we also need to draw back
    # the y-spine for both axes.
    if not float_contrast:
        rawdata_axes.set_xlim(contrast_axes.get_xlim())
    og_xlim_raw = rawdata_axes.get_xlim()
    rawdata_axes.vlines(
        og_xlim_raw[0], og_ylim_raw[0], og_ylim_raw[1], **redraw_axes_kwargs
    )

    og_xlim_contrast = contrast_axes.get_xlim()

    if float_contrast:
        xpos = og_xlim_contrast[1]
    else:
        xpos = og_xlim_contrast[0]

    og_ylim_contrast = contrast_axes.get_ylim()
    contrast_axes.vlines(
        xpos, og_ylim_contrast[0], og_ylim_contrast[1], **redraw_axes_kwargs
    )

    if show_delta2:
        if plot_kwargs["delta2_label"] is not None:
            delta2_label = plot_kwargs["delta2_label"]
        elif effect_size == "mean_diff":
            delta2_label = "delta - delta"
        else:
            delta2_label = "deltas' g"
        delta2_axes = contrast_axes.twinx()
        delta2_axes.set_frame_on(False)
        delta2_axes.set_ylabel(delta2_label, fontsize=fontsize_delta2label)
        og_xlim_delta = contrast_axes.get_xlim()
        og_ylim_delta = contrast_axes.get_ylim()
        delta2_axes.set_ylim(og_ylim_delta)
        delta2_axes.vlines(
            og_xlim_delta[1], og_ylim_delta[0], og_ylim_delta[1], **redraw_axes_kwargs
        )
