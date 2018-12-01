from selenium import webdriver
from time import sleep
import os


def us_rent():
    mypath = os.path.join(os.getcwd(),"data")
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



