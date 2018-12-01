from arcgis.geocoding import geocode
from arcgis.gis import GIS
import pandas as pd
import Point_v1


def crawl(file):
    gis = GIS()
    map = gis.map("United States")
    map

    job_df = pd.read_csv(Point_v1.CONSULTING_FILE).append(pd.read_csv(Point_v1.DS_FILE)).append(
        pd.read_csv(Point_v1.SDE_FILE))

    company_loc_df = pd.DataFrame(columns=('company', 'city', 'state', 'longitude', 'latitude'))

    for i in range(0, len(job_df)):
        column = {}
        if pd.isna(job_df.iloc[i]['location']):
            state == []
            state = geocode(job_df.iloc[i]['location'])
        if state == []:
            geo = geocode(job_df.iloc[i]['company'])
            if geo == []:
                column['longitude'] = na
                column['latitude'] = na
                column['city'] = na
                column['state'] = na
            else:
                column['longitude'] = geo[0]['location']['x']
                column['latitude'] = geo[0]['location']['y']
                column['city'] = geo[0]['attributes']['City']
                column['state'] = geo[0]['attributes']['RegionAbbr']
        else:
            geo = geocode(job_df.iloc[i]['company'], state[0]['extent'])
            if geo == []:
                column['longitude'] = state[0]['location']['x']
                column['latitude'] = state[0]['location']['y']
                column['city'] = state[0]['attributes']['City']
                column['state'] = state[0]['attributes']['RegionAbbr']

            else:
                column['longitude'] = geo[0]['location']['x']
                column['latitude'] = geo[0]['location']['y']
                column['city'] = geo[0]['attributes']['City']
                column['state'] = geo[0]['attributes']['RegionAbbr']
        column['company'] = job_df.iloc[i]['company']
        company_loc_df.loc[i] = column
    company_loc_df.to_csv(file, encoding='utf-8', index=False)

def geo_clean(file):
    data = pd.read_csv(file,index = False)
    df = data.dropna().groupby(['state'],as_index=False)['state'].agg({'cnt':'count'})
    df = df.iloc[1:]
    df['cnt'] = pd.to_numeric(df['cnt']).astype(float)
    return df