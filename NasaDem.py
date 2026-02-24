

import rasterio
from rasterio.warp import transform

vrt_path = "C:/Users/karlj/Desktop/nasadem_all/nasadem.vrt"
def query(vrt_path, points_lonlat):
    with rasterio.open(vrt_path) as src:
        # Reproject input lon/lat -> dataset CRS if needed
        if src.crs and src.crs.to_string() != "EPSG:4326":
            lons, lats = zip(*points_lonlat)
            xs, ys = transform("EPSG:4326", src.crs, lons, lats)
            pts = list(zip(xs, ys))
        else:
            pts = points_lonlat

        # Sample band 1
        vals = [v[0] for v in src.sample(pts)]
        return vals