import matplotlib as mpl
import numpy as np

def texfigsize(scale):
    fig_width_pt = 469.755                          # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (np.sqrt(5.0)-1.0)/2.0            # Aesthetic ratio (you could change this)
    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
    fig_height = fig_width*golden_mean              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size

pgf_with_latex = {                      # setup matplotlib to use latex for output
    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex
    "text.usetex": True,                # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "axes.labelsize": 10,               # LaTeX default is 10pt font.
    "font.size": 10,
    "legend.fontsize": 8,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "xtick.direction": 'out',
    "ytick.direction": 'out',
    "figure.figsize": texfigsize(0.9),     # default fig size of 0.9 textwidth
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble
        ]
    }

clearsans = {
    "font.family": "Clear Sans",
    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "font.size": 6,
    "axes.titlesize" : 8,
    "legend.fontsize": 6,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "xtick.direction": 'out',
    "ytick.direction": 'out',
    "xtick.minor.visible": False,
    "ytick.minor.visible": False,
    #"figure.figsize": texfigsize(0.9),     # default fig size of 0.9 textwidth
    }

#mpl.rcParams.update(pgf_with_latex)
mpl.rcParams.update(clearsans)

def texax(ax,twinx=None):
    SPINE_COLOR = 'gray'

    for spine in ['top']:
        ax.spines[spine].set_visible(False)

    for spine in ['left', 'bottom','right']:
        ax.spines[spine].set_color(SPINE_COLOR)
        ax.spines[spine].set_linewidth(0.5)

    ax.xaxis.set_ticks_position('bottom')
    if twinx is None:
        ax.yaxis.set_ticks_position('left')
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_tick_params(direction='out', color=SPINE_COLOR)

    return ax
