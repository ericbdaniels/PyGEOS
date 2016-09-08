'''
Python module to store reusable functions 
=========================================

pygeos is a Python module for storing reusable functions related to plotting, data processing 
and file conversion for geoscience related tasks. These tasks include interfacing with open source Python packages,
GSLIB, Paraview, and Geosoft. 
'''
__version__ = '1.01'

# Load necessary modules
import os, sys
sys.path.insert(0, os.path.abspath(".."))
#__all__ = ["io", "PA", "utils", "plot"]

from pygeos import io, PA, utils, plot