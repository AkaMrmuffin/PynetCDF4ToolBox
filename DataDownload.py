#--------------------------------------------------------------------
# Name:ECMWF Data Downloading tool
# 
# Author: Mozhou Gao
# 
# Created: 03/12/2017
#
# Purpose of script:Download the data from different datasets of ECMWF by using ECMWF API 
#                   more details can be found on https://software.ecmwf.int/wiki/display/WEBAPI/ECMWF+Web+API+Home
#
# Inputs:Multiple ECMWF data retriving keys 
#
# Outputs:downloaded data
#
#--------------------------------------------------------------------
#!/usr/bin/env python
#import ECMWFDataServer from ECMWF API
from ecmwfapi import ECMWFDataServer
import arcpy
#connect to the ECMWF server
server = ECMWFDataServer()
#set the arcpy input for each required key
stream_name = arcpy.GetParameterAsText(0)
levtype = arcpy.GetParameterAsText(1)
parameter = arcpy.GetParameterAsText(2)
dataset = arcpy.GetParameterAsText(3)
step = arcpy.GetParameterAsText(4)
grid = arcpy.GetParameterAsText(5)
time = arcpy.GetParameterAsText(6)
date = arcpy.GetParameterAsText(7)
datatype = arcpy.GetParameterAsText(8)
dclass = arcpy.GetParameterAsText(9)
area = arcpy.GetParameterAsText(10)
FM = arcpy.GetParameterAsText(11)
target = arcpy.GetParameterAsText(12)
#retrive the data based on the inputs
server.retrieve({
    'stream'    : stream_name,
    'levtype'   : levtype,
    'param'     : parameter,
    'dataset'   : dataset,
    'step'      : step,
    'grid'      : grid,
    'time'      : time,
    'date'      : date,
    'type'      : datatype,
    'class'     : dclass,
    'area'      : area,
    'format'    : FM,
    'target'    : target
 })



