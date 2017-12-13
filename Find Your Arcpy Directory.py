#-------------------------------------------------------------------------------
# Name: Find Your Arcpy Directory 

# Purpose:Locate the directory of your python side package
#
# Author: ESRI     
#
# Source: https://blogs.esri.com/esri/arcgis/2012/09/06/a-simple-approach-for-including-3rd-party-python-libraries-with-your-scripts/
# Created:     06/09/2017
# Copyright:   ESRI
# Input: side package's name 
# Output: return the input side package' path/directory in your computer 
#-------------------------------------------------------------------------------

def find_module(modulename, filename=None):
    """Finds a python module or package on the standard path.
       If a filename is specified, add its containing folder
       to the system path.

       Returns a string of the full path to the module/package."""
    import imp
    import sys
    import os

    full_path = []
    if filename:
        full_path.append(os.path.dirname(os.path.abspath(filename)))
    full_path += sys.path
    fname = imp.find_module(modulename, full_path)
    return fname[1]


print find_module('arcpy')