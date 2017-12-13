# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 18:34:38 2017

@author: mozhou
"""

import arcpy
import netCDF4 as nc4
import numpy as np
import pandas as pd

inputdata = arcpy.GetParameterAsText(0)
data = nc4.Dataset(inputdata,'r+')
Dim_keys = data.dimensions.keys()
Var_keys = data.variables.keys()

time = data .variables['time'][...]
lat = data .variables['latitude'][...]
lon = data .variables['longitude'][...]
key = arcpy.GetParameterAsText(1)
var = data.variables[key][...]
X,Y = np.meshgrid(lon,lat)

x = arcpy.GetParameterAsText(2)
y = arcpy.GetParameterAsText(3)

coor = (float(x),float(y))

It = np.nditer([X,Y],flags = ['f_index'])
for e1,e2 in It:
    if e1 == coor[0] and e2 == coor[1]: 
		Target_index = It.index
		arcpy.AddMessage(Target_index)
        
t = len(time)

Var_list = []

Tindex =np.arange(t)
for i in Tindex :
    var_layer = var[i,:,:]
    l = np.nditer(var_layer,flags = ['f_index'])
    for ele in l:
        if  l.index == Target_index:
            Var_list.append(ele)
            
Var_df = pd.DataFrame({"Time": Tindex,
                       key + " Value":Var_list },
                    columns = ["Time", key + " Value"])

OutputPath = arcpy.GetParameterAsText(4)
Var_df.to_csv(OutputPath)