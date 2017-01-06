extract:
	rm -rf geodata/*.geojson
	ogr2ogr -f GeoJSON -s_srs epsg:25832 -t_srs epsg:4326 geodata/landkreise.geojson geodata/vg250-ew_3112.utm32s.shape.ebenen/vg250-ew_ebenen/vg250_krs.dbf
	ogr2ogr -f GeoJSON -s_srs epsg:25832 -t_srs epsg:4326 geodata/gemeinden.geojson geodata/vg250-ew_3112.utm32s.shape.ebenen/vg250-ew_ebenen/vg250_gem.dbf
	ogr2ogr -f GeoJSON -s_srs epsg:25832 -t_srs epsg:4326 geodata/bundeslaender.geojson geodata/vg250-ew_3112.utm32s.shape.ebenen/vg250-ew_ebenen/vg250_lan.dbf

download:
	mkdir -p geodata
	curl "http://sg.geodatenzentrum.de/web_download/vg/vg250-ew_3112/utm32s/shape/vg250-ew_3112.utm32s.shape.ebenen.zip" > geodata/vg.zip
	unzip -d geodata geodata/vg.zip


all: download extract
