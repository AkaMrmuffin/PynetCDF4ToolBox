# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 22:15:57 2017

@author: mozhou
"""
import arcpy
import netCDF4 as nc4
import numpy as np
import pandas as pd
arcpy.env.workspace = arcpy.GetParameterAsText(0)
Dim_num = []
Var_name = []
Var_units = []
Var_shape = []
Var_max = []
Var_min = [] 
Var_mean = []
Var_std = []
IPname = arcpy.GetParameterAsText(1)
testD = nc4.Dataset(IPname,'r')
OPname = arcpy.GetParameterAsText(2)
des = open(OPname,'w')
Dim_key = testD.dimensions.keys()
line1 = ",".join(Dim_key)
des.write('The File Dimension \n')
des.write(line1)
des.write('\n')
for ele in Dim_key:  
    dim = testD.dimensions[ele]
    size = str(len(dim))
    Dim_num.append(size)
line2 = ','.join(Dim_num)
des.write(line2)

Var_key = testD.variables.keys()
des.write('\n')
des.write('Thre are ' + str(len(Var_key))+ ' variables in this netcdf file!' + '\n')
des.write('\n')
for e in Var_key:
    vard = testD.variables[e]
    var = testD.variables[e][:]
    var_flat = var.flatten()
    Var_units.append(vard.units)
    Var_name.append(vard.long_name)
    Var_shape.append(vard.shape)
    Var_max.append(max(var_flat))
    Var_min.append(min(var_flat))
    Var_mean.append(np.mean(var_flat))
    Var_std.append(np.std(var_flat))

time = testD.variables['time'][:]
lat = testD.variables['latitude'][:]
lon = testD.variables['longitude'][:]

tempres = time[1] - time [0]
latres = abs(lat[1] - lat[0])
longres = abs(lon[1]-lon[0])

des.write('The Temporal Resolusion is: ' + str(tempres)+ '\n' )
des.write('The Spatial Resolusion is: ' + str(latres) + ' X ' + str(longres) + '\n')	
des.write('\n')
NCDF = pd.DataFrame({'Variables Key': Var_key,
                                'Variables Name': Var_name,
                                'Variables Units': Var_units,
                                'Variables Shape': Var_shape,
                                'Min': Var_min,
                                'Max': Var_max,
                                'Mean': Var_mean,
                                'Standard Deviation': Var_std},
                    columns =['Variables Key','Variables Name','Variables Units',
                              'Variables Shape','Min','Max','Mean','Standard Deviation'])
NCstring = NCDF.to_string() 


   
des.write(NCstring) 
des.close()
arcpy.AddMessage(NCDF)
testD.close()
arcpy.AddMessage('Thanks for using NETCDF data describing tool!!')