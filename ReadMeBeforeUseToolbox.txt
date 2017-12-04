Term Project Assignment - GEOG 567 Introduction to Programming in GIS

This toolbox include the three tools 
	1. The ECMWF data downloading tool
	2. The Netcdf/Grid Data reading tool 
	3. The Weather Data Mapping tool 
	
	
For running the toolbox smoothly, the needed modules show as follow: 

	1. Numpy 
	2. Pandas
	2. ArcPy
	3. netCDF4
	
############The Data Downloading tool uses the ECMWF API############

ECMWF is an independent intergovernmental organisation that support many deffierent weather datasets, which includes Forecasts, analyses, climate re-analyses,reforecasts. 

The 6 most popular datasets are ERA5, ERA-Interim, ERA-Interim/Land, ERA-20C, ERA-20CM, and CERA-20C 

click this(https://www.ecmwf.int/) for more details 

Instead of downloading the data from website, the python ECMWF Web API can help their user directly dowanload data using python.

This link  (https://software.ecmwf.int/wiki/display/WEBAPI/How+to+retrieve+ECMWF+Public+Datasets) is a step by step guide of using ECMWF web API. 

If you dont want to read the official guide, please follow my brief ECMWF-Web API setup guide: 
1. regist an account at ECMWF (https://apps.ecmwf.int/registration/) and log in your account (https://apps.ecmwf.int/auth/login/)
2. get your key from ECMWF (https://api.ecmwf.int/v1/key/)
3. copy your key and paste it in any txt file 
	your key should looks like this: 
	{
		"url"   : "https://api.ecmwf.int/v1",
		"key"   : "XXXXXXXXXXXXXXXXXXXXXX",
		"email" : "mozhou.gao@example.ca"
	}
4. open the txt file with Notepad++ and save as the file to your home directory (e.g. my home directory is C:\Users\mozhou.gao) and rename file to .ecmwfapirc

5. install ecmwfapi python library 

    pip install https://software.ecmwf.int/wiki/download/attachments/56664858/ecmwf-api-client-python.tgz
	
    if you don't know pip install please check this link (https://packaging.python.org/tutorials/installing-packages/)
	
    Alternatively, you can mannully dowanload the file by using this https://software.ecmwf.int/wiki/download/attachments/56664858/ecmwf-api-client-python.tgz 
	and unzip it to your PYTHONPATH, if you don't know your PYTHONPATH please check (https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7) 
	or you can run the 'Find Your Arcpy Directory.py' script to automaticlly find your PYTHONPATH.

6. Congrets!!! you are good to use the Data download tool!!!!!

############Downloading Guide for netCDF4 package ############

1. you can find the all the .whl file for different operating system on https://pypi.python.org/pypi/netCDF4

2. you can mannually install the package to your PYTHONPATH or you can just sue 'pip install'. 
	
3. In you need to install other required packages you can find all of extension package on https://www.lfd.uci.edu/~gohlke/pythonlibs/

4. After installing the netCDF4 package, you are good to use all the tools. 










