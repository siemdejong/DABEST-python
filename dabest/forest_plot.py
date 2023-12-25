# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/API/forest_plot.ipynb.

# %% auto 0
__all__ = ['load_plot_data', 'extract_plot_data', 'forest_plot']

# %% ../nbs/API/forest_plot.ipynb 5
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
from typing import List, Optional, Tuple, Union


# %% ../nbs/API/forest_plot.ipynb 6
def load_plot_data(contrasts: List, 
                   effect_size: str = 'mean_diff', 
                   contrast_type: str = 'delta2') -> List:
    """
    Loads plot data based on specified effect size and contrast type.

    Parameters:
    contrasts (List): List of contrast objects.
    effect_size (str): Type of effect size ('mean_diff', 'median_diff', etc.).
    contrast_type (str): Type of contrast ('delta2', 'mini_meta').

    Returns:
    List: Contrast plot data based on specified parameters.
    """
    effect_attr_map = {
        'mean_diff': 'mean_diff',
        'median_diff': 'median_diff',
        'cliffs_delta': 'cliffs_delta',
        'cohens_d': 'cohens_d',
        'hedges_g': 'hedges_g'
    }

    contrast_attr_map = {
        'delta2': 'delta_delta',
        'mini_meta': 'mini_meta'
    }

    effect_attr = effect_attr_map.get(effect_size)
    contrast_attr = contrast_attr_map.get(contrast_type, 'delta_delta')

    if not effect_attr:
        raise ValueError(f"Invalid effect_size: {effect_size}")

    return [getattr(getattr(contrast, effect_attr), contrast_attr) for contrast in contrasts]

def extract_plot_data(contrast_plot_data, contrast_labels):
    """ Extracts bootstrap, difference, and confidence intervals based on contrast labels. """
    if contrast_labels == 'mini_meta':
        attribute_suffix = 'weighted_delta'
    else:
        attribute_suffix = 'delta_delta'

    bootstraps = [getattr(result, f'bootstraps_{attribute_suffix}') for result in contrast_plot_data]
    differences = [result.difference for result in contrast_plot_data]
    bcalows = [result.bca_low for result in contrast_plot_data]
    bcahighs = [result.bca_high for result in contrast_plot_data]

    return bootstraps, differences, bcalows, bcahighs

def forest_plot(contrasts: List, 
                selected_indices: Optional[List] = None, 
                analysis_type: str = 'delta2', 
                xticklabels: Optional[List] = None,
                effect_size: str = 'mean_diff', 
                contrast_labels: str = 'delta_delta', 
                ylabel: str = 'ΔΔ Volume (nL)',
                plot_elements_to_extract: Optional[List] = None, 
                title: str = 'ΔΔ Forest', 
                custom_palette: Optional[Union[dict, list, str]] = None,  # Custom color palette parameter
                fontsize: int = 20, 
                violin_kwargs: Optional[dict] = None, 
                marker_size: int = 20, 
                ci_line_width: float = 2.5,
                zero_line_width: int = 1, 
                remove_spines: bool = True, 
                ax: Optional[plt.Axes] = None,
                additional_plotting_kwargs: Optional[dict] = None, 
                rotation_for_xlabels: int = 45, 
                alpha_violin_plot: float = 0.4) -> plt.Figure:
    """
    Generates a customized forest plot using contrast objects from DABEST-python package or similar.
    
    Parameters:
    contrasts (List): List of contrast objects.
    selected_indices (Optional[List]): Indices of contrasts to be plotted, if not all.
    analysis_type (str): Type of analysis ('delta2', 'minimeta').
    xticklabels (Optional[List]): Custom labels for x-axis ticks.
    effect_size (str): Type of effect size ('mean_diff', 'median_diff', etc.).
    contrast_labels (str): Labels for each contrast.
    ylabel (str): Label for the y-axis.
    plot_elements_to_extract (Optional[List]): Plot elements to be extracted for custom plotting.
    title (str): Title of the plot.
    ylim (Tuple[float, float]): y-axis limits.
    custom_palette (Optional[Union[dict, list, str]]): Custom palette for violin plots.
    fontsize (int): Font size for labels.
    violin_kwargs (Optional[dict]): Additional kwargs for violin plots.
    marker_size (int): Size of the markers for mean differences.
    ci_line_width (float): Line width for confidence intervals.
    zero_line_width (int): Width of the zero line.
    remove_spines (bool): Whether to remove the plot spines.
    ax (Optional[plt.Axes]): Axes object to plot on, if provided.
    additional_plotting_kwargs (Optional[dict]): Additional plotting parameters.
    rotation_for_xlabels (int): Rotation angle for x-axis labels.
    alpha_violin_plot (float): Transparency level for violin plots.

    Returns:
    plt.Figure: The matplotlib figure object with the plot.
    """
    from .plot_tools import halfviolin
    # Load plot data
    contrast_plot_data = load_plot_data(contrasts, effect_size, analysis_type)

    # Extract data for plotting
    bootstraps, differences, bcalows, bcahighs = extract_plot_data(contrast_plot_data, contrast_labels)

    # Infer the figsize based on the number of contrasts
    all_groups_count = len(contrasts)
    each_group_width_inches = 2.5  # Adjust as needed for width
    base_height_inches = 4  # Base height, adjust as needed
    height_inches = base_height_inches
    width_inches = each_group_width_inches * all_groups_count
    fig_size = (width_inches, height_inches)

    # Create figure and axes if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=fig_size)
    else:
        fig = ax.figure

    # Zero line
    ax.plot([0, len(contrasts) + 1], [0, 0], 'k', linewidth=zero_line_width)

    # Violin plots with customizable colors
    violin_kwargs = violin_kwargs or {'widths': 0.5, 'vert': True, 'showextrema': False, 'showmedians': False}
    v = ax.violinplot(bootstraps, **violin_kwargs)
    halfviolin(v, alpha=alpha_violin_plot)  # Apply halfviolin from dabest

    # Handle the custom color palette
    if custom_palette:
        if isinstance(custom_palette, dict):
            violin_colors = [custom_palette.get(c, sns.color_palette()[0]) for c in contrasts]
        elif isinstance(custom_palette, list):
            violin_colors = custom_palette[:len(contrasts)]
        elif isinstance(custom_palette, str):
            if custom_palette in plt.colormaps():
                violin_colors = sns.color_palette(custom_palette, len(contrasts))
            else:
                raise ValueError(f"The specified `custom_palette` {custom_palette} is not a recognized Matplotlib palette.")
    else:
        violin_colors = sns.color_palette()[:len(contrasts)]

    for patch, color in zip(v['bodies'], violin_colors):
        patch.set_facecolor(color)
        patch.set_alpha(alpha_violin_plot)

    # Effect size dot and confidence interval
    for k in range(1, len(contrasts) + 1):
        ax.plot(k, differences[k - 1], 'k.', markersize=marker_size)
        ax.plot([k, k], [bcalows[k - 1], bcahighs[k - 1]], 'k', linewidth=ci_line_width)

    # Custom settings
    ax.set_xticks(range(1, len(contrasts) + 1))
    ax.set_xticklabels(xticklabels or range(1, len(contrasts) + 1), rotation=rotation_for_xlabels, fontsize=fontsize)
    ax.set_xlim([0, len(contrasts) + 1])
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.set_title(title, fontsize=fontsize)
    ylim = (min(bcalows)-0.25, max(bcahighs)+0.25)
    ax.set_ylim(ylim)

    # Remove spines if requested
    if remove_spines:
        for spine in ax.spines.values():
            spine.set_visible(False)

    # Additional customization
    if additional_plotting_kwargs:
        ax.set(**additional_plotting_kwargs)

    return fig
