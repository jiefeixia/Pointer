from selenium import webdriver
from time import sleep
import os
import pandas as pd

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


def download(file):
    download_path = os.path.join(os.getcwd(), "data")
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_path}
    options.add_experimental_option('prefs', prefs)
    try:
        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        driver.get('https://www.zillow.com/home-values/')
        sleep(2)
        driver.find_element_by_link_text("View Data Table").click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//a[text()="Download Full Data"]').click()
        sleep(5)
    except Exception:
        print("Limited updates. Please try again later.")

    # clean data
    df = pd.read_excel("data//united-states.xls", skiprows=2)
    df = df.iloc[1:, [0, 3]]

    df['rent'] = df["Current"].replace(',', '')
    df['rent'] = df["Current"].replace('--', 0)
    df['state'] = df["Region Name"].map(us_state_abbrev)

    df.to_csv(file)
