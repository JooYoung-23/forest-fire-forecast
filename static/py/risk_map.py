from flask import render_template
import geopandas as gpd

def view_risk_map():
	path_GW_SGG = 'static/data/Gangwon_regions/Gangwon_regions.shp'
	gdf = gpd.read_file(path_GW_SGG)
	return (render_template('risk_map.html', data=gdf.to_json()))