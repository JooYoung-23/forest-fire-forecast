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

import visualize_utils as vis_util

def Clipper_with_min_max(raster, vector, output_dir_prefix, data_name, min_max):
    with rio.open(raster) as src:
        min_val = min_max[0]
        max_val = min_max[1]
        # Read Shapefile
        with fiona.open(vector, "r", encoding="utf-8") as shapefile:
            source_crs= shapefile.crs  # Example: EPSG 4326 (WGS84)
            target_crs = src.crs
            transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)
            for feature in shapefile:
                state_name = feature['properties']['SGG_NM'] + '/'
                geometry = transform(transformer.transform, shape(feature['geometry']))
                out_image, out_transform = mask.mask(src, [geometry], crop=True, nodata=np.nan)
                # Check if the output image is not empty
                if np.isnan(out_image).all():
                    raise RuntimeError("Empty output")
                out_meta = src.profile
                out_meta.update({"height": out_image.shape[1],
                                    "width": out_image.shape[2],
                                    "transform": out_transform})

                # Generate output filename based on the feature index
                output_dir_name = f'{output_dir_prefix}{state_name}'
                vis_util.is_exist_dir(output_dir_name)
                output_filename = f'{output_dir_name}{data_name}'
                
                # Save the clipped image as a separate file
                with rio.open(output_filename+'.tif', "w", **out_meta) as dest:
                    dest.write(out_image)
                    
                vis_util.show_map(output_filename+'.tif', output_filename, image_size=1, color='turbo', limit=[min_val, max_val])
                os.remove(output_filename+'.tif')

def Cliper_execute_weather(dir_prefix, data_list, min_max_list):
    vis_util.is_exist_dir(dir_prefix)
    Raster = [dir_prefix + x + '.tif' for x in data_list]
    Output_resol = [dir_prefix + x + '_resol.tif' for x in data_list]
    Output_clear = [dir_prefix + x + '_clear.tif' for x in data_list]
    Vector =  "../../WEB/static/DB/reference/vector_reference/vector_reference.shp"
    RefImage = "../../WEB/static/DB/reference/proj_reference.tif"

    for i in range(len(data_list)):
        #match_resolution(Raster[i], Output_resol[i], RefImage)
        #clear_boundary_using_arr(Output_resol[i], Output_clear[i], RefImage)
        Clipper_with_min_max(Raster[i], Vector, dir_prefix, data_list[i], min_max_list[i])
        Output_png = Raster[i][:Raster[i].rfind('.')]
        vis_util.show_map(Raster[i], Output_png, image_size=1, color='turbo', limit= min_max_list[i])

    file = os.listdir(dir_prefix)
    del_file = [dir_prefix + x for x in file if x.endswith('.tif') or x.endswith('xml')]
    [os.remove(x) for x in del_file]

def Cliper_execute_result(dir_prefix, data_list, min_max_list):
    vis_util.is_exist_dir(dir_prefix)
    Arr = [dir_prefix + x + '.npy' for x in data_list]
    Raster = [dir_prefix + x + '.tif' for x in data_list]
    Vector =  "../../WEB/static/DB/reference/vector_reference/vector_reference.shp"
    RefImage = "../../WEB/static/DB/reference/proj_reference.tif"

    for i in range(len(data_list)):
        vis_util.array_to_image(np.load(Arr[i]), Raster[i], RefImage)
        Clipper_with_min_max(Raster[i], Vector, dir_prefix, data_list[i], min_max_list[i])
        Output_png = Raster[i][:Raster[i].rfind('.')]
        vis_util.show_map(Raster[i], Output_png, image_size=1, color='turbo', limit= min_max_list[i])

    file = os.listdir(dir_prefix)
    del_file = [dir_prefix + x for x in file if x.endswith('.tif') or x.endswith('xml')]
    [os.remove(x) for x in del_file]


### Example
# 파일 제자리에 위치 시키고 날짜만 지정하면 됨 > 날짜 = 디렉토리 이름
date = "202305252100"

weather_dir = "../../WEB/static/DB/weather/" + date + '/'
weather_list = ['temp', 'rainfall', 'wind', 'humidity']
weather_min_max_list = [(-14.7, 37.8), (0, 19), (0, 20.9), (2, 100)]

result_dir = "../../WEB/static/DB/result/" + date + '/'
result_list = ['result']
result_min_max_list = [(0, 1)]

Cliper_execute_weather(weather_dir, weather_list, weather_min_max_list)
Cliper_execute_result(result_dir, result_list, result_min_max_list)