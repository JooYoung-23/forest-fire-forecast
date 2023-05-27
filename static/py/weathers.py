
import datetime
import os
import urllib3
import requests
import pandas as pd
import time
from tqdm.auto import tqdm
from datetime import datetime, timedelta,date
from glob import glob
import rasterio
from pyidw import idw 
import geopandas as gpd #
import matplotlib.pyplot as plt
from osgeo import gdal, ogr
from update_function import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'

def update_weather():
	current_time = datetime.datetime.now().time()
	# print("Current time:", current_time)
	# print("type:", type(current_time))
	# print("str:", str(current_time))
	time = str(current_time)
	hour = time[0:2]
	minute = time[3:5]
	
	if (os.fork()):
	
		f_path = f'database/'
		os.makedirs(f"{f_path}", exist_ok=True)
		today = date.today()
		features=['humidity','wind_sp','rainfall','temp']

		inputdate=str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2)

		times = hour.zfill(2) + "30"
		filenames=iffuture(inputdate,times,future_loc)
		
		# 보간법 
		interpolation(filenames,1)
		os._exit(0)
	os.wait()

	from modeling import modeling

	fulldate = str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2) + hour.zfill(2) + "30"
	file_name = datetime.strptime(fulldate, "%Y%m%d%H%M")
	file_1 = (file_name + timedelta(hours=1, minutes=30)).strftime("%Y%m%d%H%M")
	file_2 = (file_name + timedelta(hours=2, minutes=30)).strftime("%Y%m%d%H%M")
	file_3 = (file_name + timedelta(hours=3, minutes=30)).strftime("%Y%m%d%H%M")
	t_1=file_1[-4:]
	t_2=file_2[-4:]
	t_3=file_3[-4:]

	for input_date in range([t_1, t_2, t_3]):
		if (os.fork()):
			modeling(input_date)
			os._exit(0)
		os.wait()