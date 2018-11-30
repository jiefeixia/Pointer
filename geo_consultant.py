from arcgis.geocoding import geocode
from arcgis.gis import GIS
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode,iplot
init_notebook_mode(connected=True)


def geo_consultant():
    gis = GIS()
    map = gis.map("United States")
    map
    consultants = pd.read_csv("jobs_consultant.csv")

    data = pd.DataFrame(columns=('company','city','state','longitude','latitude'))

    for i in range(0, len(consultants)):
        dic ={}
        if pd.isna(consultants.iloc[i]['location']):
            state ==[]
        else:
            state = geocode(consultants.iloc[i]['location'])
        if state == []:
            geo = geocode(consultants.iloc[i]['company'])
            if geo == []:
                dic['longitude'] = na
                dic['latitude'] = na
                dic['city'] = na
                dic['state'] = na
            else:
                dic['longitude'] = geo[0]['location']['x']
                dic['latitude'] = geo[0]['location']['y']
                dic['city'] = geo[0]['attributes']['City']
                dic['state'] = geo[0]['attributes']['RegionAbbr']
        else:
            geo = geocode(consultants.iloc[i]['company'],state[0]['extent'])
            if geo == []:
                dic['longitude'] = state[0]['location']['x']
                dic['latitude'] = state[0]['location']['y']
                dic['city'] = state[0]['attributes']['City']
                dic['state'] = state[0]['attributes']['RegionAbbr']

            else:
                dic['longitude'] = geo[0]['location']['x']
                dic['latitude'] = geo[0]['location']['y']
                dic['city'] = geo[0]['attributes']['City']
                dic['state'] = geo[0]['attributes']['RegionAbbr']
        dic['company'] = consultants.iloc[i]['company']
        data.loc[i] = dic
    data.to_csv("geo_consultants.csv", encoding='utf-8', index=False)

def consultant_clean():
    data = pd.read_csv("geo_consultants.csv",index = False)
    df = data.dropna().groupby(['state'],as_index=False)['state'].agg({'cnt':'count'})
    df = df.iloc[1:]
    df['cnt'] = pd.to_numeric(df['cnt']).astype(float)
    return df

def consultant_map():
    df = geo_clean()

    dat = dict(type='choropleth',
            colorscale = 'Viridis',
            locations = df['state'],
            z = df['cnt'],
            locationmode = 'USA-states',
            marker = dict(line = dict(color = 'rgb(255,255,255)',width = 2)),
            colorbar = {'title':"Count of jobs"}
            )
    layout = dict(title = 'Consultant Job Distribution around US',
             geo = dict(scope = 'usa',
                       showlakes = True))

    choromap = go.Figure(data = [dat],layout = layout)
    iplot(choromap,validate=False)












