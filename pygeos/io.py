#!/usr/bin/env python

"""

module for import/export functions

NOTE: many functions require the Geosoft GX plug-in
Currently commented out b/c I am no longer working with geosoft regularly.

"""

__author__ = "Eric Daniels"


import os
#import geosoft.gx as gx 
import pandas as pd
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import pygslib as gs 



#os.environ['GX_GEOSOFT_BIN_PATH'] = 'C:\\Program Files (x86)\\Geosoft\\bin'
#ctx = gx.GXContext.create('test','Geosoft Inc.')

#read grid from geosoft binary to pandas dataframe
def read_gxgrid(GridPath,name):
    """
    Read geosoft grid to pandas dataframe

    Args:

        GridPath: Filepath of Geosoft grid

        name: Name for column header in pandas dataframe

    Returns:
        Pandas DataFrame
    """

    GridObj = gx.GXIMG.create_file(ctx, gx.GS_TYPE_DEFAULT,GridPath, gx.IMG_FILE_READORWRITE)
    PgObj = GridObj.geth_pg()
    tempfile = name+'.txt'
    WaObj = gx.GXWA.create(ctx,tempfile,0)
    PgObj.write_wa(WaObj, 0,0,0,0,'-1e21')
    df = pd.read_csv(tempfile,header=None, sep=r"\s+")
    df.columns = [name]
    return df 


def to_gxgrid(df,name, griddef):
    """
    Convert Pandas DataFrame to Geosoft grid

    Args:

        df: Pandas DataFrame to be Gridded
        name: variable name
        griddef: pygslib GridDef object to set grid definition

    Returns:
        (GXgrd): Geosoft grid (.grd)

        Note: this function does not set the projection 
    """

    nrows=griddef.nx
    ncols=griddef.ny
    df.to_csv(name, sep=' ', index=False, header=False)
    RaObj = gx.GXRA.create(ctx,name) #use os.remove after?
    PgObj = gx.GXPG.create(ctx,ncols,nrows,5)
    PgObj.read_ra(RaObj,5,0,0,0,name) #throwing error
    GridObj = gx.GXIMG.create_new_file(ctx,5,1,nrows,ncols,name+'.grd')
    GridObj.set_pg(PgObj)
    GridObj.set_info(griddef.xsiz, griddef.ysiz, griddef.xmn, griddef.ymn,0)
    print(name, ' Grid File created')

#read ply 


def read_ply(filepath):
    """
    Read polygon from .ply file

    Args:
        filepath: filepath for polygon file

    Returns:
        (tuple): tuple containing:
        
        |  ply: pandas DataFrame containing XY coordinates for verticies
        |  patch:  matplotlib patch for use in plotting
        

    """
    ply = pd.read_csv(filepath, skiprows=[0,1,2,3,4,5], delim_whitespace=True, 
        names=['X','Y'], header=None)
    path = Path(ply.values,codes=None, closed =True)
    patch = patches.PathPatch(path,edgecolor='black', facecolor='none', lw=2)
    return(ply,patch)


#import LAS files - returns tops dictionary and pandas dataframe


def read_LAS(FilePath):
    """
    Read LAS files to pandas Dataframe and dictionary of tops 

    Args:
    
        Filepath: location of LAS file
    
    Returns:
        (tuple): tuple containing:

        |  TopsDict: dictionary containing tops 
        |  WellData: Pandas DataFrame with log data 
        |  

        NOTE: Not all LAS files are the same, this function was designed using Petra exported files.
        LAS files from other software may yield and error.            
    """
    topsdict={} #dictionary for storing tops
    Data = []
    with open(FilePath,'r') as f:
        #get tops
        for line in f:
            if line.strip().startswith('#TOP NAME'):
                f.readline()
                break
        for line in f:
            if line.strip().startswith('~A'):
                colnames = line.split()[1:]
                break
            (key, val) = line.split()
            topsdict[key]=val
        #read columns to pandas dataframe
        for line in f:
            row = line.split()
            Data.append(row)
        WellData = pd.DataFrame.from_records(Data)
        WellData = WellData.astype(float)
        WellData.columns=colnames
        return TopsDict, WellData

#import pangeos g2d file, returns pygslib GridDef
def read_g2d (FilePath):
    """
    Read Pangeos g2d file to PyGSLIB GridDef object 

    Args:
    
        Filepath: location of .g2d file

    Returns:
        (gs.GridDef): PyGSLIB griddef object

    """
    with open(FilePath, 'r') as f:
        gs.GridDef.nx, gs.GridDef.xmn, gs.GridDef.xsiz = [int(x) for x in f.readline().split()]
        gs.GridDef.ny, gs.GridDef.ymn, gs.GridDef.ysiz = [int(x) for x in f.readline().split()]
        gs.GridDef.nz, gs.GridDef.zmn, gs.GridDef.zsiz = 1, 0.5, 1
        if f.readline().strip() != 'XY':
            gs.GridDef.nz, gs.GridDef.zmn, gs.GridDef.zsiz = [int(x) for x in f.readline().split()]
    return gs.GridDef

#import ASCII tabular from Petra

#import gxdatabase
#export gxdatabase

#vtk import/export
#gslib import/export

#read in GSLIB files with griddef in 2nd line
def read_GSLIB(FilePath, griddef):
    """
        Read GSLIB gridded file with grid definition in header.

        Args:

            FilePath: Location of .dat GSLIB file 
            
            griddef: pyGSLIB gs.GridDef object 

        Returns:
            (tuple): tuple containing:

            |  griddef: pyGSLIB griddef object with grid definition read from header
            |  data: Pandas DataFrame with Grid(s)
    """
    with open(FilePath,'r') as f:
        title = f.readline()
        line2 = f.readline().split() 
        ncols = int(line2[0])
        line2 = [float(i) for i in line2[1:]]
        griddef.nx, griddef.ny, griddef.nz = line2[0], line2[1], line2[2]
        griddef.xmn, griddef.ymn, griddef.zmn = line2[3], line2[4], line2[5]
        griddef.xsiz, griddef.ysiz, griddef.zsiz = line2[6], line2[7], line2[8]
        columns = []
        for i in range(0,ncols):
            columns.append(f.readline().strip())
        f.close()
        data = pd.read_csv(FilePath, skiprows=ncols+2, names=columns, delim_whitespace=True)
        #data.columns = columns
        return griddef, data
