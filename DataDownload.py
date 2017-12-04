
#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
import arcpy
server = ECMWFDataServer()
arcpy.env.workspace = arcpy.GetParameterAsText(0)
stream_name = arcpy.GetParameterAsText(1)
levtype = arcpy.GetParameterAsText(2)
parameter = arcpy.GetParameterAsText(3)
dataset = arcpy.GetParameterAsText(4)
step = arcpy.GetParameterAsText(5)
grid = arcpy.GetParameterAsText(6)
time = arcpy.GetParameterAsText(7)
date = arcpy.GetParameterAsText(8)
datatype = arcpy.GetParameterAsText(9)
dclass = arcpy.GetParameterAsText(10)
area = arcpy.GetParameterAsText(11)
FM = arcpy.GetParameterAsText(12)
target = arcpy.GetParameterAsText(13)
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



