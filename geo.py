from arcgis.geocoding import geocode
from arcgis.gis import GIS
import pandas as pd
import Point_v1


def crawl(file):
    gis = GIS()
    map = gis.map("United States")
    map

    # read all kinds of job files
    job_df = pd.read_csv(Point_v1.CONSULTING_FILE).append(
        pd.read_csv(Point_v1.DS_FILE)).append(
        pd.read_csv(Point_v1.SDE_FILE))

    company_loc_df = pd.DataFrame()
    company_loc_df["company"] = job_df["company"].unique()
    geo_info = company_loc_df["company"].apply(lambda company: geocode(company)[0] if geocode(company) else None)

    company_loc_df['longitude'] = geo_info.apply(lambda info: info["location"]["x"] if info else None)
    company_loc_df['latitude'] = geo_info.apply(lambda info: info["location"]["y"] if info else None)
    company_loc_df['city'] = geo_info.apply(lambda info: info['attributes']['City'] if info else None)
    company_loc_df['state'] = geo_info.apply(lambda info: info['attributes']['RegionAbbr'] if info else None)

    company_loc_df.to_csv(file, encoding='utf-8', index=False)
