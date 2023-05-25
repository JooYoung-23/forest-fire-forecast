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