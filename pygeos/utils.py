#!/usr/bin/env python
__author__ = "Eric Daniels"


# -*- coding: utf-8 -*-
# @Author: edaniels
# @Date:   2015-10-09 08:11:39
# @Last Modified by:   edaniels
# @Last Modified time: 2016-07-08 14:05:18


"""
This module contains commonly used utilities and other miscellaneous functions
"""


import pandas as pd 
import numpy  as np
import os
import shutil
import scipy
import scipy.cluster.vq
import scipy.spatial.distance



#Get Coordinates - based on PyGSLIB GridDef. Returns pd DataFrame of coordinates
#could tweak to join coords with existing dataframe
def getcoords (GridDef):
    """
    Generate Pandas DataFrame of XYZ coordinates based on grid definition

    Args:
        GridDef: pyGSLIB Grid Definition object 

    Returns:
        coords: Pandas DataFrame with the columns X, Y and Z
    """
    coordslist = []
    for i in range(0,int(GridDef.nz)):
        for j in range(0,int(GridDef.ny)):
            for k in range(0,int(GridDef.nx)):
                x = GridDef.xmn+GridDef.xsiz*k
                y = GridDef.ymn+GridDef.ysiz*j
                z = GridDef.zmn+GridDef.zsiz*i
                coordslist.append((x, y , z))
    coords = pd.DataFrame.from_records(coordslist, columns=['X','Y','Z'])
    return coords

# two functions for finding the index of a given point in a grid and extracting data from grid

def getidx(points, griddef):
    """
    Return the index of a given point in a grid 
    Best used with df.apply() function in pandas

    Args:

        points: Pandas DataFrame including columns labeled X and Y 
        
        griddef: pyGSLIB Grid Definition object

    Returns:
        (int): index value for location in grid

    """
    X_idx = int(((points['X']-float(griddef.xmn))/float(griddef.xsiz)) + 1.5)
    Y_idx = int(((points['Y']-float(griddef.ymn))/float(griddef.ysiz)) + 1.5)
    idx = X_idx + (Y_idx-1)*float(griddef.nx)
    return idx

def gridExtract(ptxy, griddef, gridDF):
    """
    Uses getidx to extract gridded data based on point locations

    Args: 

        ptxy: Pandas DataFrame containing X Y columns of coordinates

        griddef: pyGSLIB Grid Definition object

        gridDF: Pandas Dataframe containing grid(s)

    Returns:
        (Pandas DataFrame): Values extracted from grid(s) at XY locations
    """
    indicies = ptxy.apply(getidx, args=([griddef]), axis=1)
    idxExtract = gridDF.loc[indicies,:]
    return idxExtract






def gap(data, refs=None, nrefs=20, ks=range(1,11)):
    """
    Compute the Gap statistic for an nxm dataset in data.
    Either give a precomputed set of reference distributions in refs as an (n,m,k) scipy array,
    or state the number k of reference distributions in nrefs for automatic generation with a
    uniformed distribution within the bounding box of data.
    Give the list of k-values for which you want to compute the statistic in ks.
    """
    dst = scipy.spatial.distance.euclidean
    shape = data.shape
    if refs==None:
        tops = data.max(axis=0)
        bots = data.min(axis=0)
        dists = scipy.matrix(scipy.diag(tops-bots))


        rands = scipy.random.random_sample(size=(shape[0],shape[1],nrefs))
        for i in range(nrefs):
            rands[:,:,i] = rands[:,:,i]*dists+bots
    else:
        rands = refs

    gaps = scipy.zeros((len(ks),))
    refs = scipy.zeros((len(ks),))
    disps = scipy.zeros((len(ks),))
    for (i,k) in enumerate(ks):
        (kmc,kml) = scipy.cluster.vq.kmeans2(data, k)
        disp = sum([dst(data[m,:],kmc[kml[m],:]) for m in range(shape[0])])

        refdisps = scipy.zeros((rands.shape[2],))
        for j in range(rands.shape[2]):
            (kmc,kml) = scipy.cluster.vq.kmeans2(rands[:,:,j], k)
            refdisps[j] = sum([dst(rands[m,:,j],kmc[kml[m],:]) for m in range(shape[0])])
        gaps[i] = scipy.mean(scipy.log(refdisps))-scipy.log(disp)
        refs[i] = refdisps
        disps[i] = disp
    return refs, disps, gaps