import threading
import schedule
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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
import ray


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
import numpy as np
import json
from multiprocessing import Process

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'

future_loc=pd.read_csv("C:/Users/user/project/forest-fire-forecast/static/py/future_loc.csv",encoding='cp949') # 현재, 미래 데이터 크롤링 
past_loc=pd.read_csv("C:/Users/user/project/forest-fire-forecast/static/py/aws_loc_list.csv")  # 과거 데이터 크롤링 
f_path = f'database/'

def future_weather_crawling(date,times,locn):
    url = 'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    
    params ={'serviceKey' : '3imQf/ygL+vTqRcXZ19hAwVhJhVDxZ2yRGtaRQPk/F3rFSVB2Kvu7LFfoGVhB4rYfTVk2kILGAhhJvmu9kQUzA==', #AuthenticationKey
			'pageNo' : '1',
			'numOfRows' : '1000',
			'dataType' : 'JSON', 
			'base_date' : date, 
			'base_time' : times, 
			'nx' : locn[1], 
			'ny' : locn[0], 
            }
    for i in range(5):  # 최대 5번까지 시도
        try:
            response = requests.get(url, params=params,verify=False)
            try:
                json_obj = json.loads(response.content)
                try:
                    json_obj=json_obj["response"]["body"]["items"]["item"]       
                    return json_obj
                except:
                    print("Retry1")
                    print(json_obj)
                    time.sleep(5)
            except:
                print(response.content)
                try:
                    json_obj = json.loads(response.content)
                    print(response,json_obj)
                    print("Retry2")
                    time.sleep(5)
                except json.JSONDecodeError:
                    time.sleep(2)
                    continue  
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            print(f'Network ERROR')
            time.sleep(2)
    return np.nan

def past_weather_crawling(date,locn):
    
    url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList'
    startDt=datetime.strptime(date[:8], '%Y%m%d') # 시작날짜
    startHh = datetime.strptime(date[8:], '%H')   # 시작시간
    endHh = (startHh + timedelta(hours=1))        # 시작날짜 + 1 (23같은경우 00이 되게 하기위해서 timedelta 이용)
    
    if(endHh.strftime('%H:%M:%S').split(':')[0]=='00'):
        endDt=(startDt + timedelta(days=1))
        
    else:
        endDt=startDt # endhh==00이면 시작날짜와 종료날짜가 달라야함. 22일 23시와 23일 00시 이런식.

    startDt=startDt.strftime('%Y%m%d')
    startHh=startHh.strftime('%H:%M:%S').split(':')[0]
    endDt=endDt.strftime('%Y%m%d')
    endHh=endHh.strftime('%H:%M:%S').split(':')[0]
    
    params ={'serviceKey' : '3imQf/ygL+vTqRcXZ19hAwVhJhVDxZ2yRGtaRQPk/F3rFSVB2Kvu7LFfoGVhB4rYfTVk2kILGAhhJvmu9kQUzA==', #AuthenticationKey
			'pageNo' : '1',
			'numOfRows' : '10',
			'dataType' : 'JSON', 
			'dataCd' : 'ASOS', 
			'dateCd' : 'HR', 
			'startDt' : startDt, #startdate
			'startHh' : startHh, #starttime
			'endDt' : endDt, # end date
			'endHh' : endHh, # end time
			'stnIds' : locn 
            }
    for i in range(5):  # 최대 5번까지 시도
        try:
            response = requests.get(url, params=params,verify=False)
            try:
                json_obj = json.loads(response.content)
                try:
                    json_obj=json_obj["response"]["body"]["items"]["item"][0]
                    times=json_obj['tm']
                    humidity=json_obj['hm']
                    windspeed=json_obj['ws']
                    winddir=json_obj['wd']
                    rain=json_obj['rn']
                    temp=json_obj['ta']              
                    return times, humidity, windspeed, winddir, rain, temp
                except:
                    print("Retry1")
                    print(json_obj)
                    time.sleep(5)
            except:
                print(response.content)
                try:
                    json_obj = json.loads(response.content)
                    print(response,json_obj)
                    print("Retry2")
                    time.sleep(5)
                except json.JSONDecodeError:
                    time.sleep(2)
                    continue   
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            print(f'오류 발생 재시도')
            time.sleep(2)
    return np.nan,np.nan,np.nan,np.nan,np.nan,np.nan  

def iffuture(date,times,loc_list):
	print("iffuture times = :", times)
	result_list = []
    
	fulldate=date+times
	file_name = datetime.strptime(fulldate, "%Y%m%d%H%M")
	file_1 = (file_name + timedelta(hours=1, minutes=30)).strftime("%Y%m%d%H%M")
	file_2 = (file_name + timedelta(hours=2, minutes=30)).strftime("%Y%m%d%H%M")
	file_3 = (file_name + timedelta(hours=3, minutes=30)).strftime("%Y%m%d%H%M")
    
	for i in tqdm(range(len(loc_list))):
		loc=(loc_list['격자 Y'].iloc[i],loc_list['격자 X'].iloc[i])

		result=pd.DataFrame(future_weather_crawling(date,times,loc))

		t_1=file_1[-4:]
		t_2=file_2[-4:]
		t_3=file_3[-4:]

		time_list = [t_1,t_2,t_3]

		output = result[result['fcstTime'].isin(time_list)]
		output = output.pivot(index=['baseDate', 'baseTime', 'fcstDate', 'fcstTime', 'nx', 'ny'], columns='category', values='fcstValue').reset_index()

		output.drop(['LGT','VEC','SKY','UUU','VVV','PTY'],axis=1,inplace=True)
		output.columns=['baseDate', 'baseTime', 'fcstDate', 'fcstTime', 'nx', 'ny','습도','강수량','기온','풍속']
		result_list.append(output)

	test = pd.concat(result_list, ignore_index=True)

	tmp1=test[test['fcstTime']==t_1].reset_index(drop=True)
	tmp2=test[test['fcstTime']==t_2].reset_index(drop=True)
	tmp3=test[test['fcstTime']==t_3].reset_index(drop=True)

	tmp1.to_csv(f'{f_path}/{file_1}.csv',index=False,encoding='cp949')
	tmp2.to_csv(f'{f_path}/{file_2}.csv',index=False,encoding='cp949')
	tmp3.to_csv(f'{f_path}/{file_3}.csv',index=False,encoding='cp949')
    
	return [file_1,file_2,file_3]
    
def ifpast(date,times,loc_list):
	fulldate=date+times
    
	loc_num=loc_list['지점번호']
	file=fulldate+'00'

	tmp=pd.DataFrame(columns=['location information', 'longitude','latitude','time','humidity','wind speed','wind direction','precipitation','temperature'])
	for j in tqdm(range(len(loc_num))):
		result=[loc_num[j],loc_list['lon'][j],loc_list['lat'][j]]
		result.extend(past_weather_crawling(fulldate,loc_num[j])) 
		tmp = pd.concat([tmp, pd.DataFrame([result], columns=tmp.columns)], ignore_index=True)
	tmp.to_csv(f"{f_path}/{file}.csv",index=False,encoding='cp949')
    
	return [file]

def interpolation(filenames,tense):
	f_path = f'database/'
	os.makedirs(f"{f_path}", exist_ok=True)
	today = date.today()
	features=['humidity','wind_sp','rainfall','temp']
	for i in range(len(filenames)):
		image_list=[]
		data=pd.read_csv(f'{f_path}/{filenames[i]}.csv',encoding='cp949')
        
		if(tense==1):
			data.drop(['baseDate','baseTime','fcstDate','fcstTime'],axis=1,inplace=True)
			data.columns=['nx','ny','humidity','rainfall','temp','wind_sp']
			data['rainfall'] = data['rainfall'].replace('강수없음', '0mm')
			data['rainfall']=[j[:-2] for j in data['rainfall']]
			data['rainfall']=data['rainfall'].fillna(0)
			data['rainfall']=data['rainfall'].astype('float')
			data = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.ny, data.nx)).drop(['nx','ny'],axis=1)
		else:
			data.columns=['loc_info', 'longitude', 'latitude', 'time','humidity', 'wind_sp', 'wind_dr', 'rainfall','temp']
			data.dropna(subset=['time'], inplace=True)
			data['rainfall']=data['rainfall'].fillna(0)
			data=data.dropna()
			data.drop(['loc_info','time'],axis=1,inplace=True)
			data = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.longitude, data.latitude))
            
		data.to_file(f'tmp.shp')

		for j in range(len(features)):
			idw.idw_interpolation(
				input_point_shapefile=f'tmp.shp', # 보간하고자 하는 shp 파일 
				extent_shapefile="boundary/boundary.shp", # 경계 shp 파일(현재 강원도)
				column_name=features[j], # 보간하고자 하는 feature 이름. 
				power=2, # 거리 가중치 계수 
				search_radious=8, # 검색하고자 하는 범위 
				output_resolution=400, # 결과물 해상도 
			)
			image=rasterio.open(f'tmp_idw.tif')
			image=pd.DataFrame(image.read(1))
			image_list.append(image)
            
		temps,hums,rains,winds=[],[],[],[]
		for j in range(len(image.index)):
			for k in range(len(image.columns)):
				hums.append(image_list[0].iloc[j][k])
				rains.append(image_list[1].iloc[j][k])
				temps.append(image_list[2].iloc[j][k])
				winds.append(image_list[3].iloc[j][k])
                
		climates = {'temp': temps, 'hum': hums, 'rain': rains, 'wind': winds}
		df = pd.DataFrame(climates)
		df=df.replace(32767.0,-9999)
		#df.to_csv(f"{f_path}/{date}{file[epoch]}_idw.csv",index=False)
		x_train=[]
		for j in tqdm(range(len(df))):
			x_train.append(np.array(df.loc[j, ['temp','hum','rain','wind']]).astype(float))
		climate = np.array(x_train)
		np.save(f'{f_path}/{filenames[i]}.npy', climate)
		#os.remove(f'{f_path}/{date}{file[epoch]}.csv')
	os.remove(f"tmp.shp")
	os.remove(f"tmp.cpg")
	os.remove(f"tmp.dbf")
	os.remove(f"tmp.shx")
	os.remove(f"tmp_idw.tif")
	os.remove(f'{f_path}/{filenames[i]}.csv')
    
def image_to_array(InputImage):
	Image = gdal.Open(InputImage, gdal.GA_Update)
	array = Image.ReadAsArray()
	print(array.shape)
	return array



def update_weather():
	current_time = datetime.now().time()
	print(current_time)
	# print("Current time:", current_time)
	# print("type:", type(current_time))
	# print("str:", str(current_time))
	time = str(current_time)
	hour = time[0:2]
	minute = time[3:5]
	
	f_path = f'database/'
	os.makedirs(f"{f_path}", exist_ok=True)
	today = date.today()
	features=['humidity','wind_sp','rainfall','temp']
	def test1():
		# f_path = f'database/'
		# os.makedirs(f"{f_path}", exist_ok=True)
		# today = date.today()
		# features=['humidity','wind_sp','rainfall','temp']

		inputdate=str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2)

		times = str(int(hour)-1).zfill(2)  + "30"
		# times = hour.zfill(2)  + "30"
		print("times = ", times)
		filenames=iffuture(inputdate,times,future_loc)
		
		# 보간법 
		interpolation(filenames,1)
		return (filenames)
	
	#proc = Process(target=lambda: test1())
	#proc.start()
	#proc.join()
	filenames = test1()

	#if (os.fork() == 0):
	#
	#	f_path = f'database/'
	#	os.makedirs(f"{f_path}", exist_ok=True)
	#	today = date.today()
	#	features=['humidity','wind_sp','rainfall','temp']
#
#		inputdate=str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2)
#
#		times = hour.zfill(2) + "30"
#		filenames=iffuture(inputdate,times,future_loc)
#		
#		# 보간법 
#		interpolation(filenames,1)


	fulldate = str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2) + hour.zfill(2) + "30"
	file_name = datetime.strptime(fulldate, "%Y%m%d%H%M")
	file_1 = (file_name + timedelta(hours=1, minutes=30)).strftime("%Y%m%d%H%M")
	file_2 = (file_name + timedelta(hours=2, minutes=30)).strftime("%Y%m%d%H%M")
	file_3 = (file_name + timedelta(hours=3, minutes=30)).strftime("%Y%m%d%H%M")
	t_1=file_1[-4:]
	t_2=file_2[-4:]
	t_3=file_3[-4:]

## start modeling
	import tensorflow as tf
	import numpy as np
	from osgeo import gdal, ogr

	def array_to_image(InputArr, OutputImage, RefImage):
		Image = gdal.Open(RefImage, gdal.GA_Update)
		ImageArr = Image.ReadAsArray()
    
		open(OutputImage, 'w')
		Output = gdal.GetDriverByName('GTiff').Create(OutputImage, ImageArr.shape[1], ImageArr.shape[0], 1, gdal.GDT_Float32)
		#writting output raster
		Output.GetRasterBand(1).WriteArray(InputArr)
		Output.SetProjection(Image.GetProjection())
		Output.SetGeoTransform(Image.GetGeoTransform())

		Image = None
		Output = None
	@ray.remote
	def modeling(inputdate):
		gpus = tf.config.list_physical_devices('GPU')
		if gpus:
			try:
				for gpu in gpus:
					tf.config.experimental.set_memory_growth(gpu, True)
					logical_gpus = tf.config.list_logical_devices('GPU')
				print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
			except RuntimeError as e:
				print(e)
		#from tensorflow.python.client import device_lib
		#device_lib.list_local_devices()

		#model = tf.keras.models.load_model("C:/Users/user/resnet_model")
		#model = tf.keras.models.load_model("C:/Users/user/fire_model/cnn24")
		model = tf.keras.models.load_model("C:/Users/user/fire_model/cnn32")
		#model = tf.keras.models.load_model("C:/Users/user/fire_model/resnet24")
	
		climate_test=np.load(f'database/{inputdate}.npy')

		Height_test=np.load('D:/new_test24/Height_test.npy')
		NDVI_test=np.load('D:/new_test24/NDVI_test.npy')
		Slope_test=np.load('D:/new_test24/Slope_test.npy')
		landuse_test=np.load('D:/new_test24/Landuse_test.npy')
		popden_test=np.load('D:/new_test24/Pop_test.npy')
	
		x_test = {
			#'forest_input': forest_train,
			'height_input': Height_test,
			'ndvi_input': NDVI_test,
			'slope_input': Slope_test,
			'landuse_input': landuse_test,
			'popden_input': popden_test,
			'climate_input':climate_test
		}
	
		y_pred = model.predict(x_test)
	
		result_arr = np.zeros((278, 400))
		x = 0
		for i in range(278):
			for j in range(400):
				result_arr[i, j] = y_pred[x]  # 결과 배열에 값 추가
				x += 1
	
		# np.save(f'database/result/res24_result/{inputdate}.npy', result_arr)
		InputArr=result_arr
		OutputImage=f'static/images/result{inputdate[0:4]}_{inputdate[4:6]}_{inputdate[6:8]}_{inputdate[8:10]}.tif'
		RefImage='boundary/boundary_blank_resized.tif'
		array_to_image(InputArr, OutputImage, RefImage)
## end modeling

	# Start ray
	ray.init(ignore_reinit_error=True, num_cpus = os.cpu_count()-3)
	
	obj_refs = []
	for input_date in filenames:
		obj_refs.append(modeling.remote(input_date))
	while obj_refs:
		done, obj_refs = ray.wait(obj_refs)
		ray.get(done[0])
	
	ray.shutdown()

	# for input_date in filenames:
	#	modeling(input_date)

	#	proc = Process(target=modeling, args=(input_date))
	#	proc.start()
	#	proc.join()	

	#	if (os.fork() == 0):
	#		modeling(input_date)
	#		os._exit(0)
	#	os.wait()



	
def run_threaded(job_func):
	job_thread = threading.Thread(target=job_func)
	job_thread.start()

def schedule_thread():
	while True:
		schedule.run_pending()

def scheduling_data_update():
	print("test")
	schedule.every().hour.at(":33").do(run_threaded, update_weather)
	schedule.every(1).minutes.do(update_weather)
	thread = threading.Thread(target=schedule_thread)
	thread.start()