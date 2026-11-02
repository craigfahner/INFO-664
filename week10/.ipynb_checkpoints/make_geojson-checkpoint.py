"""Prepare the two small GeoJSON files used by week10_scratch.ipynb.

Students don't need to run this (or install geopandas). It is the instructor's recipe for the files:

* districts_120th.geojson: U.S. House districts for the 2026 election (Census Bureau, 120th Congress),
  each with an id like "TX-12".
* nyc_districts.geojson: NYC community districts from the Housing Database CSV, each with its
  `commntydst` code and the longitude/latitude of its center.

Needs: pip install pandas geopandas
"""

import pandas as pd
import geopandas as gpd

# ---------------------------------------------------------------- House districts
states = pd.read_csv("https://www2.census.gov/geo/docs/reference/state.txt", sep="|", dtype=str)
states = states[~states["STUSAB"].isin(["AS", "GU", "MP", "PR", "UM", "VI"])]    # skip the territories

frames = []
for _, row in states.iterrows():
    url = f"https://www2.census.gov/geo/tiger/TIGER2026/CD/tl_2026_{row.STATE}_cd120.zip"
    shapes = gpd.read_file(url)
    shapes["state"] = row.STUSAB
    frames.append(shapes)

shapes = pd.concat(frames, ignore_index=True)

# drop "not defined" areas (water) and D.C.'s non-voting seat; at-large districts become district 1
shapes = shapes[shapes["CD120FP"].str.fullmatch(r"\d{2}") & (shapes["CD120FP"] != "98")].copy()
shapes["district"] = shapes["CD120FP"].astype(int).clip(lower=1)
shapes["id"] = shapes["state"] + "-" + shapes["district"].astype(str)

shapes = shapes.to_crs(4326)
shapes["geometry"] = shapes.geometry.simplify(0.01, preserve_topology=True)      # about 1 km
shapes[["id", "geometry"]].to_file("districts_120th.geojson", driver="GeoJSON")

# ---------------------------------------------------------------- NYC community districts
nyc = pd.read_csv("Housing_Database_by_Community_District_20261102.csv", thousands=",")
geometry = gpd.GeoSeries.from_wkt(nyc["the_geom"], crs="EPSG:2263")                # New York State Plane, in feet
districts = gpd.GeoDataFrame({"commntydst": nyc["commntydst"]}, geometry=geometry)

center = districts.geometry.centroid.to_crs(4326)
districts = districts.to_crs(4326)
districts["lon"] = center.x.round(5)
districts["lat"] = center.y.round(5)
districts["geometry"] = districts.geometry.simplify(0.0002)                         # about 20 meters
districts.to_file("nyc_districts.geojson", driver="GeoJSON")
