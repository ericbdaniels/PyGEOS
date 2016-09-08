#!/usr/bin/env python
__author__ = "Eric Daniels"

# -*- coding: utf-8 -*-
# @Author: edaniels
# @Date:   2015-09-29 14:51:30
# @Last Modified by:   edaniels
# @Last Modified time: 2016-07-28 09:10:03


"""
Module for common plotting needs
"""


import matplotlib.pyplot as plt 
import matplotlib.style as style 
import matplotlib.cm as cm 
import pandas as pd 
import numpy as np 
import seaborn as sns
import scipy.stats as stats

#scatter plots and correlation matrix plot

def corr_plot(df, outfl=None, color='dimgray'):
    """
    Generate a matrix plot for examining pairwise relationships between datatypes

    Args:

        df: Pandas DataFrame with data

        outfl: file path for saved plot (optional)

        color: color for points on scatter plots
    """
    with style.context('bmh', after_reset=True):
        nrows, ncols = df.shape
        corrvals = df.corr()
        fig, axes = plt.subplots(ncols, ncols, figsize=(15,12))
        for j in range(ncols):
            for i in range(ncols):
                if i>j:
                    axes[i,j].scatter(df[[j]], df[[i]],c=color, edgecolors="none")
                    axes[i,j].grid(False)
                    axes[i,j].tick_params(axis='x', top='off')
                    axes[i,j].tick_params(axis='y', right='off')
                    ylabels = axes[i,j].get_yticklabels()
                    for ylabel in ylabels:
                        ylabel.set_fontsize(8)
                    xlabels = axes[i,j].get_xticklabels()
                    for xlabel in xlabels:
                        xlabel.set_rotation(45)
                        xlabel.set_fontsize(8)
                    if j>0:
                        axes[i,j].set_yticks([])
                        
                    if i!=ncols-1:
                        axes[i,j].set_xticks([])
                if i==j:
                    df[[i]].hist(normed=1, ax=axes[i,j])
                    #axes[i,j].hist(df.iloc[:,i], normed=1)
                    axes[i,j].set_title(df.columns[i])
                    axes[i,j].grid(False)
                    axes[i,j].tick_params(axis='x', top='off')
                    #axes[i,j].set_ylim(0,1)
                    axes[i,j].set_yticks([])
                    xlabels = axes[i,j].get_xticklabels()
                    for xlabel in xlabels:
                        xlabel.set_rotation(45)
                        xlabel.set_fontsize(8)
                if i<j:
                    corrval = corrvals.iloc[i,j]
                    corrval2 = (corrval/2)+0.5
                    axes[i,j].set_axis_bgcolor(cm.coolwarm(corrval2))
                    axes[i,j].annotate(np.round(corrval,2),xy=(0.5,0.5), xycoords='axes fraction',va='center', ha='center', fontsize=18)
                    axes[i,j].grid(False)
                    axes[i,j].set_xticks([])
                    axes[i,j].set_yticks([])
        fig.tight_layout(pad=0.05)
        if outfl is not None:
        	plt.savefig(outfl)
        plt.show()
        plt.close()


# log plot based on LAS file reader - requires Pandas datafrme of data and topsdict
def log_plot(Data, columns, topsdict, top, bottom, cmap=cm.jet, cutoff=None, outfl=None, show=True, returnfig=False):
    """
    Plot well log information from LAS file

    Args:

        Data: Pandas DataFrame with log data 

        columns: columns within DataFrame to plot 

        topsdict: a dictionary of tops from which top and bottom will be selected 

        top: top formation for plot 

        bottom: bottom formation for plot 

        cmap: colormap (default is jet)

        cutoff: cutoff value (optional)

        outfl: filepath for saved plot (optional)

        show: True/False to show plot (default: True)

        returnfig: True/False to return figure as object, useful for color mapping / legend

    """

    Data = Data[(float(topsdict[bottom])>Data['DEPT'].astype(float))&(Data['DEPT'].astype(float)>float(topsdict[top]))]
    fig, ax = plt.subplots(1,len(columns), figsize = (len(columns)*5, 20))
    
    if len(columns)>1:
        for i in range(0,len(columns)):
            color=cmap(i/len(columns))
            ax[i-1].plot(Data[columns[i-1]], Data['DEPT'], color=color)
            ax[i-1].invert_yaxis()
            ax[i-1].set_title(columns[i-1])
            if cutoff is not None:
                if cutoff[i-1] is not None: ax[i-1].axvline(x=cutoff[i-1], linewidth=0.5, color='black')
    else:
        ax.plot(Data[columns], Data['DEPT'])
        ax.invert_yaxis()
    
    if show is True:
        plt.show()
    
    if outfl is not None:
        plt.savefig(outfl)
        
    if returnfig is True:
        return returnfig
    
    plt.close()



#Fancy cross-plot to show grid data vs training data from well locations
def fancy_xplot(GridData, WellData,var1, var2, outfl, show=True, figsize=(15,15)):
    """
    Cross plotting function used to portray gridded data and extracted scattered data on the same plot 
    Useful to show relationship between grids and data actually used in training for PA methods 

    Args:

        GridData: Pandas DataFrame of gridded data 

        WellData: Scattered well data extracted from grid locations (same variable names as GridData)

        var1, var2 : variables for crossplotting 

        outfl: filepath for saving figure

        show: True/False to show figure 

        figsize: set figure size (default: 15x15)
    """

    sns.set_style('white')

    left, width = 0.1 , 0.65

    bottom, height = 0.1, 0.65
    bottom_h = left_h = left+width+0.01

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width,0.2]
    rect_histy = [left_h, bottom, 0.2, height]

    plt.figure(1, figsize=figsize)

    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx,sharex=axScatter)
    axHisty = plt.axes(rect_histy,sharey=axScatter)

    axScatter.scatter(GridData[var1], GridData[var2],edgecolor='White', c='cornflowerblue')
    axScatter.scatter(WellData[var1], WellData[var2], c='crimson')
    axHistx.hist([GridData[var1].dropna(), WellData[var1]], normed=1, stacked=False, bins=30, color=['cornflowerblue','tomato'])
    axHisty.hist([GridData[var2].dropna(), WellData[var2]], normed=1, stacked=False,color=['cornflowerblue','tomato'], bins=30,orientation='horizontal')

    axHistx.grid(False)

    axHisty.grid(False)
    axHistx.set_title(var1)
    axHisty.set_title(var2,rotation=270,x=1.1,y=0.5)
    sns.despine()
    #plt.tight_layout()
    plt.savefig(outfl)
    if show is True:
        plt.show()


def probplt(dataSeries, outfl=None, color='black'):
    
    
    if dataSeries.dropna().size > 0:
        fig, ax1 = plt.subplots(figsize=(8,6))
        # Calculate quantiles for probplt
        (quantiles, values), (slope, intercept, r) = stats.probplot(dataSeries.dropna(), dist=stats.norm)

        #plot results
        ax1.plot(values, quantiles, '.', c=color)
        ax1.plot(quantiles * slope + intercept, quantiles, 'black', lw=0.5, ls='dashed')
        
        #define ticks
        ticks_perc=[0.01, 0.1, 0.2, 1, 5, 10, 20, 50, 80, 90, 95, 99, 99.8, 99.9, 99.99]

        #transfrom them from precentile to cumulative density
        ticks_quan=[-stats.norm.ppf(i/100.) for i in ticks_perc]
    
        #assign new ticks
        ax1.set_yticks(ticks_quan)
        ax1.set_yticklabels(ticks_perc)
        ax1.set_xscale('log')
        ax1.grid(True, which='both', alpha=0.5)  
        ax1.set_title('Probabilty Plot')
        ax1.set_ylabel('Cumulative Probability')
        ax1.set_xlabel(dataSeries.name)
        
    
        plt.figtext(0.5, 0.95, dataSeries.name, size=20, weight='bold', ha='center')
        if outfl is not None:
                plt.savefig(outfl)
        plt.show()
               