from arcgis.geocoding import geocode
from arcgis.gis import GIS
import pandas as pd

def geo_sde():
    gis = GIS()
    map = gis.map("United States")
    map
    sde = pd.read_csv("jobs_sde.csv")


    data3 = pd.DataFrame(columns=('company','city','state','longitude','latitude'))

    for i in range(0, len(sde)):
        dict ={}
        if pd.isna(sde.iloc[i]['location']):
            state ==[]
        else:
            state = geocode(sde.iloc[i]['location'])
        if state == []:
            geo = geocode(sde.iloc[i]['company'])
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
            geo = geocode(sde.iloc[i]['company'],state[0]['extent'])
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
        dict['company'] = sde.iloc[i]['company']
        data3.loc[i] = dict
    data3.to_csv("geo_sde.csv", encoding='utf-8', index=False)

