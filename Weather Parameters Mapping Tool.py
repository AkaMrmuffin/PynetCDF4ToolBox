#--------------------------------------------------------------------
# Name:NetCDF Data Mapping Tool
# 
# Author: Mozhou Gao
# 
# Created: 01/12/2017
#
# Purpose of script: Calculate the number of days UAV/drone can fly based on drone's operating 
#					temperature range, wind speed resistance, and precipitation threshold
#
# Inputs:The NetCDF data file,wind speed, temperature, and preicipitaion thresholds 
#
# Outputs:raster file (ASCII raster file) that record number of days drone can fly
#
#--------------------------------------------------------------------
#import three side packages
import arcpy
import netCDF4 as nc4
import numpy as np

#keycheck function can check whether the user input keys are correct
def keycheck (key,key_list):
    '''
    The inputs are user input key and the variable key list of input data file.
    if the user input key is a subset of the key list, the function will return true
    if not, function will return False.
    '''
    key = [key]
    a = set(key)
    b = set(key_list)
    return a.issubset(b)

def weatherfilter(var,upperl,lowerl):
    '''
    The inputs are the weather variable multidimensional array, upper limit, and lower limit.
	if the value of the cell is within inputted range, 
	that cell will become 1 (True), otherwise the value of a cell will become 0 (False).
    '''
    upperl = float(upperl)
    lowerl = float(lowerl)
    va = np.where(np.logical_and(var>=lowerl,var<=upperl))
    vb = np.where(np.logical_or(var<lowerl,var>upperl))
    var[va] = 1
    var[vb] = 0
    return var
#weathercomb function can combine 2 boolean multidimension array 
def weathercomb(var1,var2):
    '''
    The inputs include 2 boolean multidimensional arrays that returned by weatherfilter function.
    Function will check whether each cell is true for both arrays, if it is true return 1 for that cell
    if not return 0 for that cell
    '''
    comba = var1 == var2
    combb = var1<>var2
    var1[comba] = 1
    var1[combb] = 0
    return var1

#Set arcpy environment workspace (user defined)
arcpy.env.workspace = arcpy.GetParameterAsText(0)
#let user select wind, temperature, and precipitation data 
Tempdataset = arcpy.GetParameterAsText(1)
Winddataset = arcpy.GetParameterAsText(2)
Prepdataset = arcpy.GetParameterAsText(3)
#Open the .nc data using Dataset() method with read mode
WindData = nc4.Dataset(Winddataset,'r+')
TempData = nc4.Dataset(Tempdataset,'r+')
PrepData = nc4.Dataset(Prepdataset,'r+')
#read all the variable keys from different data file
WindVar_keys = WindData.variables.keys()
TempVar_keys = TempData.variables.keys()
PrepVar_keys = PrepData.variables.keys()
#concatenate all the variable keys together
List = WindVar_keys+TempVar_keys+PrepVar_keys
#extract variables from data files based on user input keys
Var1 = arcpy.GetParameterAsText(4) #Temp
Var2 = arcpy.GetParameterAsText(5)  #Uwind
Var3 = arcpy.GetParameterAsText(6)  #Vwind
Var4 = arcpy.GetParameterAsText(7)  #Precip
#check whether input keys are matching with the keys stored in data files
VarList = [Var1,Var2,Var3,Var4]
for ele in VarList:
    vc = keycheck(ele,List)
    #if yes print error message in ArcMap message window 
    if vc == False :
        arcpy.AddError('You entered Wrong Variable Key!')

#Assign variables
time = WindData.variables['time'][:]
lat = WindData.variables['latitude'][:]
lon = WindData.variables['longitude'][:]
temp = TempData.variables[Var1][:]
uwind = WindData.variables[Var2][:]
vwind = WindData.variables[Var3][:]
precip = PrepData.variables[Var4][:]
#check whether all the variables' dimension are same
if uwind.shape == vwind.shape == temp.shape == precip.shape:
    arcpy.AddMessage('Variables Dimension Checked!!!')
else:
    arcpy.AddError('Variables Dimension not Match')
    
# assign length of each dimension to variables    
t = len(time)
la = len(lat)
lo = len(lon)
#flat multidimension matrix to 1d array
#calculate the net wind speed based on wind components using pythagorean theorem
speed = (uwind**2 + vwind**2)**0.5
#convert the units of temperature to Degree celsius
temp = temp-273.15
#let user input the wind, temperature and preicipitation thresholds
Wrange = arcpy.GetParameterAsText(8)
Trange = arcpy.GetParameterAsText(9)
Prange = arcpy.GetParameterAsText(10)
Wrange = Wrange.split(',')
Trange = Trange.split(',')
Prange = Prange.split(',')
#apply the weatherfilter function
speed = weatherfilter(speed,Wrange[0],Wrange[-1])
temp = weatherfilter(temp,Trange[0],Trange[-1])
precip = weatherfilter(precip,Prange[0],Prange[-1])
#apply the weathercomb function to combine the results
#1st check wind speed and temperature 
tempC = weathercomb(speed,temp)
# then combine with precipitation
OGIfreq = weathercomb(tempC,precip)
# sum the value along time series
OGI = np.sum(OGIfreq,axis = 0)

#let user input output raster's cell size
cellsize = arcpy.GetParameterAsText(11)
cellsize = float(cellsize)
#create a latitude and longitude grid
X,Y = np.meshgrid(lon,lat)
#locate the lower left corner of the grid
lowerleftlat = Y[la-1][0]
lowerleftlong = X[la-1][0]
#let user to decide whether they want the total fly-frequency or average fly-frequency
Year = arcpy.GetParameterAsText(12)
if Year <> "":
	OGI = OGI/float(Year)
#Conver the Numpy multidimension array to ASCII raster file
myRaster = arcpy.NumPyArrayToRaster(OGI, arcpy.Point(lowerleftlong,lowerleftlat),
									cellsize,cellsize,-9999)
#user defined output raster file's path
path = arcpy.GetParameterAsText(13)
#save the raster file to that path
myRaster.save(path)
#print path to the arcpy message window
arcpy.AddMessage('The Raster Path is: ' + path)
arcpy.AddMessage('Merry Christmas!!!')
#close all the NetCDF files
WindData.close()
TempData.close()
PrepData.close()