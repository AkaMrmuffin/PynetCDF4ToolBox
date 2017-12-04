# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 00:03:04 2017

@author: mozhou
"""
import arcpy
import netCDF4 as nc4
import numpy as np

def keycheck (key,key_list):
    key = [key]
    a = set(key)
    b = set(key_list)
    return a.issubset(b)

def weatherfilter(var,upperl,lowerl):
	upperl = float(upperl)
	lowerl = float(lowerl)
	va = np.where(np.logical_and(var>=lowerl,var<=upperl))
	vb = np.where(np.logical_or(var<lowerl,var>upperl))
	var[va] = 1
	var[vb] = 0
	return var

def weathercomb(var1,var2):
    comba = var1 == var2
    combb = var1<>var2
    var1[comba] = 1
    var1[combb] = 0
    return var1
arcpy.env.workspace = arcpy.GetParameterAsText(0)
Tempdataset = arcpy.GetParameterAsText(1)
Winddataset = arcpy.GetParameterAsText(2)
Prepdataset = arcpy.GetParameterAsText(3)

WindData = nc4.Dataset(Winddataset,'r+')
TempData = nc4.Dataset(Tempdataset,'r+')
PrepData = nc4.Dataset(Prepdataset,'r+')
WindVar_keys = WindData.variables.keys()
TempVar_keys = TempData.variables.keys()
PrepVar_keys = PrepData.variables.keys()

List = WindVar_keys+TempVar_keys+PrepVar_keys

Var1 = arcpy.GetParameterAsText(4) #Temp
Var2 = arcpy.GetParameterAsText(5)  #Uwind
Var3 = arcpy.GetParameterAsText(6)  #Vwind
Var4 = arcpy.GetParameterAsText(7)  #Precip
VarList = [Var1,Var2,Var3,Var4]
for ele in VarList:
    vc = keycheck(ele,List)
    if vc == False :
        arcpy.AddError('You entered Wrong Variable Key!')


time = WindData.variables['time'][:]
lat = WindData.variables['latitude'][:]
lon = WindData.variables['longitude'][:]
temp = TempData.variables[Var1][:]
uwind = WindData.variables[Var2][:]
vwind = WindData.variables[Var3][:]
precip = PrepData.variables[Var4][:]
if uwind.shape == vwind.shape == temp.shape == precip.shape:
    arcpy.AddMessage('Variables Dimension Checked!!!')
else:
    arcpy.AddError('Variables Dimension not Match')
    
t = len(time)
la = len(lat)
lo = len(lon)
uwind_flat = uwind.flatten()
vwind_flat = vwind.flatten()

speed = (uwind_flat**2 + vwind_flat**2)**0.5
speed = speed.reshape(t,la,lo)
temp = temp-273.15
Wrange = arcpy.GetParameterAsText(8)
Trange = arcpy.GetParameterAsText(9)
Prange = arcpy.GetParameterAsText(10)
Wrange = Wrange.split(',')
Trange = Trange.split(',')
Prange = Prange.split(',')
speed = weatherfilter(speed,Wrange[0],Wrange[-1])
temp = weatherfilter(temp,Trange[0],Trange[-1])
precip = weatherfilter(precip,Prange[0],Prange[-1])
tempC = weathercomb(speed,temp)
OGIfreq = weathercomb(tempC,precip)
OGI = np.sum(OGIfreq,axis = 0)

xcell = np.absolute(lon[1] - lon[0])
ycell = np.absolute(lat[1] - lat[0])
X,Y = np.meshgrid(lon,lat)

lowerleftlat = Y[la-1][0]
lowerleftlong = X[la-1][0]
myRaster = arcpy.NumPyArrayToRaster(OGI, arcpy.Point(lowerleftlong,lowerleftlat),0.125,0.125,-9999)
path = arcpy.GetParameterAsText(11)
myRaster.save(path)
arcpy.AddMessage('The Raster Path is: ' + path)
arcpy.AddMessage('Merry Christmas!!!')
WindData.close()
TempData.close()
PrepData.close()