# Let's define some utility functions we'll want to be using for resolutions

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import scipy.stats as stats

from . import plot_util as pu


def responsePlot(x, y, figfile='', statistic='median',
                 xlabel='Cluster Calib Hits', ylabel='Cluster Energy / Calib Hits',
                 atlas_x=-1, atlas_y=-1, simulation=False, atlas_status = 'Internal', text_color = 'black', atlas_desc = '',
                 atlas_bbox = {},
                 x_min = 0.1, x_max = 1000, y_min = 0, y_max = 3.,
                 textlist=[]):
    xbin = [10**exp for exp in np.arange(-1.0, 3.1, 0.1)]
    ybin = np.arange(0., 3.1, 0.025)
    xcenter = [(xbin[i] + xbin[i+1]) / 2 for i in range(len(xbin)-1)]
    profileXMed = stats.binned_statistic(
        x, y, bins=xbin, statistic=statistic).statistic

    # to normalize, make a list as long as the number of clusters, which is 1 / number of clusters
    weights = np.ones(len(y)) / len(y)

    plt.cla()
    plt.clf()
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    plt.hist2d(x, y, weights=weights, bins=[xbin, ybin], norm=LogNorm(),zorder = -1)
    plt.plot([0.1, 1000], [1, 1], linestyle='--', color='black')
    plt.plot(xcenter, profileXMed, color='red')
    plt.xscale('log')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    pu.ampl.set_xlabel(xlabel)
    pu.ampl.set_ylabel(ylabel)
    # ampl.set_zlabel('Clusters')
    cb = plt.colorbar()
    cb.ax.set_ylabel('Fraction of Clusters')
    # plt.legend()

    pu.drawLabels(fig, atlas_x, atlas_y, simulation, textlist, atlas_status = atlas_status, color = text_color, desc = atlas_desc, bbox = atlas_bbox)

    if figfile != '':
        plt.savefig(figfile)
    plt.show()

    return xcenter, profileXMed


def stdOverMean(x):
    std  = np.std(x)
    mean = np.mean(x)
    return std / mean

def iqrOverMed(x):
    # get the IQR via the percentile function
    # 84 is median + 1 sigma, 16 is median - 1 sigma
    q84, q16 = np.percentile(x, [84, 16])
    iqr = q84 - q16
    med = np.median(x)
    return iqr / (2*med)

def resolutionPlot(x, y, figfile='', statistic='std',
                   xlabel='Cluster Calib Hits', ylabel='Energy IQR over Median',
                   atlas_x=-1, atlas_y=-1, simulation=False,
                   textlist=[]):
    xbin = [10**exp for exp in  np.arange(-1.0, 3.1, 0.1)]
    xcenter = [(xbin[i] + xbin[i+1]) / 2 for i in range(len(xbin)-1)]
    if statistic == 'std': # or any other baseline one?
        resolution = stats.binned_statistic(x, y, bins=xbin,statistic=statistic).statistic
    elif statistic == 'stdOverMean':
        resolution = stats.binned_statistic(x, y, bins=xbin,statistic=stdOverMean).statistic
    elif statistic == 'iqrOverMed':
        resolution = stats.binned_statistic(x, y, bins=xbin,statistic=iqrOverMed).statistic

    plt.cla(); plt.clf()
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    plt.plot(xcenter, resolution)
    plt.xscale('log')
    plt.xlim(0.1, 1000)
    plt.ylim(0,2)
    pu.ampl.set_xlabel(xlabel)
    pu.ampl.set_ylabel(ylabel)

    pu.drawLabels(fig, atlas_x, atlas_y, simulation, textlist)

    if figfile != '':
        plt.savefig(figfile)
    plt.show()

    return xcenter, resolution