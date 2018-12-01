import pandas as pd
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode,iplot
init_notebook_mode(connected=True)

def rent_clean(name):
    file = pd.read_csv(name,skiprows=2)
    file = file.iloc[:,[0,3]]
    file.to_csv("US_renting_cleaned.csv",index = False)
    df2 = pd.read_csv('US_renting_cleaned.csv')
    df2 = df2.iloc[1:]
    list = []
    for i in range(0,len(df2)):
        list.append(float(df2.iloc[i]['Current'].replace(',','')[1:].replace('--','0')))
    df2['rent'] = list

    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
    }

    list1 = []
    for i in range(0,len(df2)):
        list1.append(us_state_abbrev.get(df2.iloc[i]['Region Name']))
    df2['state'] = list1
    return df2

def rent_map(df2):
    data = dict(type = 'choropleth',
           colorscale = 'Viridis',
           reversescale= True,
           locations = df2['state'],
           z = df2['rent'],
           locationmode = 'USA-states',
           text = df2['Region Name'],
           marker = dict(line = dict(color = 'rgb(255,255,255)',width = 1)),
           colorbar = {'title':"Rent(yearly)"})
    layout = dict(title = 'Rent Distribution around US',
             geo = dict(scope = 'usa',
                       showlakes = True))

    choromap = go.Figure(data = [data],layout = layout)
    iplot(choromap,validate=False)
