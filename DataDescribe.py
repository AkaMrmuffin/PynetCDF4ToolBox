#--------------------------------------------------------------------
# Name:NetCDF Data Describing Tool
# 
# Author: Mozhou Gao
# 
# Created: 01/12/2017
#
# Purpose of script: Describing the attributes of data that stored in selected NetCDF data file
#                   Such as the dimensions and keys of different variables
#
# Inputs:The NetCDF data file
#
# Outputs:Text File
#
#--------------------------------------------------------------------
#Import Python side packages 
import arcpy
import netCDF4 as nc4
import numpy as np
import pandas as pd
#Create 8 empty lists for storing attributes of variables,which is easier to combine them to dataframe later  
Dim_num = []
Var_name = []
Var_units = []
Var_shape = []
Var_max = []
Var_min = [] 
Var_mean = []
Var_std = []
#set the .nc file's name to 1st input in ArcPY GUI
IPname = arcpy.GetParameterAsText(0)
# Use netCDF4's method Dataset to open the .nc file with read mode,testD wil be a nc object
testD = nc4.Dataset(IPname,'r+')
#set the output text file's name to input of ArcPy GUI
OPname = arcpy.GetParameterAsText(1)
#open the text file with write mode 
des = open(OPname,'w')
#use dimensions.keys() to read all the dimensions' key from testD
Dim_key = testD.dimensions.keys()
#join all the keys to one string and separate keys using ',' 
line1 = ",".join(Dim_key)
#write the dimension keys string to the text file
des.write('The File Dimension \n')
des.write(line1)
des.write('\n')
#append the length of each dimension to list Dim_num and join everything inthe list to a string and write in the new line of text file
for ele in Dim_key:  
    dim = testD.dimensions[ele]
    size = str(len(dim))
    Dim_num.append(size)
line2 = ','.join(Dim_num)
des.write(line2)
#use variables.keys() method to return all vairable's key's of testD to a list 
Var_key = testD.variables.keys()
des.write('\n')
#write the length of returned list in new line of text file
des.write('Thre are ' + str(len(Var_key))+ ' variables in this netcdf file!' + '\n')
des.write('\n')
#Use object.variables['key'][...]to extract dimension variables and assign it to new variables
time = testD .variables['time'][...]
lat = testD .variables['latitude'][...]
lon = testD .variables['longitude'][...]
#Calculate the temporal and spatial resolution
tempres = time[1] - time [0]
latres = abs(lat[1] - lat[0])
longres = abs(lon[1]-lon[0])
#write the temporal resolution and spatial resolution in text file
des.write('The Temporal Resolution is: ' + str(tempres)+ '\n' )
des.write('The Spatial Resolution is: ' + str(latres) + ' X ' + str(longres) + '\n')	
des.write('\n')
#Since each nc variable object has attributes (units, long_name,shape)
#Use for loop to call attributes for each variable and store them into predefined empty list
for e in Var_key:
    vard = testD.variables[e]
    Var_units.append(vard.units)
    Var_name.append(vard.long_name)
    Var_shape.append(vard.shape)
    var = testD.variables[e][...]
    #extract each variable's value and convert them to a 1D array
    var_flat = var.flatten()
    #calculate each variables maximum, minimum, and standard deviation
    Var_max.append(max(var_flat))
    Var_min.append(min(var_flat))
    Var_mean.append(np.mean(var_flat))
    Var_std.append(np.std(var_flat))
#close the NetCDF file
testD.close()
#Use pandas' DataFrame() to create a Dataframe using the pre-defined list 
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
#covert dataframe to a string
NCstring = NCDF.to_string() 
#write the converted dataframe to textfile   
des.write(NCstring) 
#clese the text file
des.close()
#print the dataframe out in ArcMap message window
arcpy.AddMessage(NCDF)
arcpy.AddMessage('Thanks for using NETCDF data describing tool!!')