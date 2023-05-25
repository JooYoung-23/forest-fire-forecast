import os
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal, ogr
import rasterio as rio
import rasterio.mask as mask
import fiona
from shapely.geometry import shape
from shapely.ops import transform
from pyproj import Proj, Transformer

def mkdir(path):
    os.makedirs(path)

def is_exist_dir(path):
    if not os.path.exists(path):
        mkdir(path)
        
def image_to_array(InputImage):
    Image = gdal.Open(InputImage, gdal.GA_Update)
    array = Image.ReadAsArray()
    print(array.shape)
    return array

def array_to_image(InputArr, OutputImage, RefImage):
    Image = gdal.Open(RefImage, gdal.GA_Update)
    ImageArr = Image.ReadAsArray()

def _STATIC_formatting_crs(crs):
    if '4326' in str(crs):
        crs = 'EPSG:4326'
    elif '5179' in str(crs):
        crs = 'EPSG:5179'
    return crs

# 시각화할래스터, 칼럼맵,사이즈, 리턴, 경로, 경로, 피쳐넘버 
def show_map(input_raster='',save_path='', image_size=1, color='', limit=''):
    with rio.open(input_raster) as image_data:
        my_matrix = image_data.read(1)
        fig, ax = plt.subplots()
        image_hidden = ax.imshow(my_matrix, cmap=color)
        plt.close()

        fig, ax = plt.subplots()
        fig.set_facecolor("w")
        fig.set_size_inches(w=image_data.width/100, h=image_data.height/100)
        image = ax.imshow(my_matrix, cmap=color, vmin=limit[0], vmax=limit[1]) # 습도의 최댓값 100, 최솟값 2, 사이 간격은 256개
        plt.axis('off')
        plt.close()
        fig.savefig(f'{save_path}.png', bbox_inches='tight', transparent=True, pad_inches=0)
    del image
    del fig
    del my_matrix
    del image_hidden
    del image_data
    return 0


def match_resolution(InputImage, OutputImage, RefImage):
    Image = gdal.Open(RefImage, gdal.GA_ReadOnly)
    output_width = Image.RasterXSize
    output_height = Image.RasterYSize

    # Construct the command string
    open(OutputImage, 'w')
    command = ['gdal_translate', '-outsize', str(output_width), str(output_height), '-r', 'bilinear', InputImage, OutputImage]

    # Run the command
    subprocess.run(command)

    # Set geotransform and projection information
    Output = gdal.Open(OutputImage)
    Output.SetGeoTransform(Image.GetGeoTransform())
    Output.SetProjection(Image.GetProjection())

    Image = None
    Output = None
        
def clear_boundary_using_arr(InputImage, OutputImage, RefImage):
    InputArr = image_to_array(InputImage)
    Image = gdal.Open(RefImage, gdal.GA_Update)
    ImageArr = Image.ReadAsArray()
    
    out_boundary_lat = []
    out_boundary_lon = []
    out_value = ImageArr[0, 0]
    for i in range(Image.RasterYSize):
        for j in range(Image.RasterXSize):
            if ImageArr[i, j] == out_value:
                out_boundary_lat.append(i)
                out_boundary_lon.append(j)
    InputArr[out_boundary_lat, out_boundary_lon] = InputArr[0, 0]
    array_to_image(InputArr, OutputImage, RefImage)