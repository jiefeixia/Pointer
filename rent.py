from selenium import webdriver
from time import sleep
import os
import pandas as pd


def download(file):
    mypath = os.path.join(os.getcwd(), "data")
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': mypath}
    options.add_experimental_option('prefs', prefs)
    try:
        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        driver.get('https://www.zillow.com/home-values/')
        sleep(2)
        driver.find_element_by_link_text("View Data Table").click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//a[text()="Download Full Data"]').click()
        sleep(5)
    except:
        print("Limited updates. Please try again later.")

    # clean data
    file = pd.read_csv(name, skiprows=2)
    file = file.iloc[:, [0, 3]]
    file.to_csv("US_renting_cleaned.csv", index=False)
    df2 = pd.read_csv('US_renting_cleaned.csv')
    df2 = df2.iloc[1:]
    list = []
    for i in range(0, len(df2)):
        list.append(float(df2.iloc[i]['Current'].replace(',', '')[1:].replace('--', '0')))
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
    for i in range(0, len(df2)):
        list1.append(us_state_abbrev.get(df2.iloc[i]['Region Name']))
    df2['state'] = list1
    df2.to_csv(file)
