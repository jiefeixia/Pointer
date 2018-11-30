from arcgis.geocoding import geocode
from arcgis.gis import GIS
import pandas as pd

def geo_ds():
    gis = GIS()
    map = gis.map("United States")
    map
    ds = pd.read_csv("jobs_ds.csv")


    data2 = pd.DataFrame(columns=('company','city','state','longitude','latitude'))

    for i in range(0, len(ds)):
        dict ={}
        if pd.isna(ds.iloc[i]['location']):
            state ==[]
        else:
            state = geocode(ds.iloc[i]['location'])
        if state == []:
            geo = geocode(ds.iloc[i]['company'])
            if geo == []:
                dict['longitude'] = na
                dict['latitude'] = na
                dict['city'] = na
                dict['state'] = na
            else:
                dict['longitude'] = geo[0]['location']['x']
                dict['latitude'] = geo[0]['location']['y']
                dict['city'] = geo[0]['attributes']['City']
                dict['state'] = geo[0]['attributes']['RegionAbbr']
        else:
            geo = geocode(ds.iloc[i]['company'],state[0]['extent'])
            if geo == []:
                dict['longitude'] = state[0]['location']['x']
                dict['latitude'] = state[0]['location']['y']
                dict['city'] = state[0]['attributes']['City']
                dict['state'] = state[0]['attributes']['RegionAbbr']

            else:
                dict['longitude'] = geo[0]['location']['x']
                dict['latitude'] = geo[0]['location']['y']
                dict['city'] = geo[0]['attributes']['City']
                dict['state'] = geo[0]['attributes']['RegionAbbr']
        dict['company'] = ds.iloc[i]['company']
        data2.loc[i] = dict
    data2.to_csv("geo_ds.csv", encoding='utf-8', index=False)

