#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
import pandas as pd


# In[2]:


ANDREW_ID = "jiefeix"
PASSWORD = "Aaply2018!"


# In[3]:


options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)


# In[4]:


driver.get("https://www.smartevals.com/SchoolList.aspx")


# In[5]:


driver.find_elements_by_css_selector('a.dxp-num[aria-label="Page 3 of 22"]')[0].click()


# In[6]:


driver.find_elements_by_xpath("//td[contains(text(), 'Carnegie Mellon University')]/..//input")[0].click()


# In[7]:


driver.find_elements_by_css_selector('#j_username')[0].send_keys(ANDREW_ID)
driver.find_elements_by_css_selector('#j_password')[0].send_keys(PASSWORD)
driver.find_elements_by_css_selector('input.loginbutton')[0].click()


# In[8]:


driver.find_elements_by_css_selector('#lnkSeeResultsImg')[0].click()
table_window = driver.window_handles[1]
driver.switch_to_window(table_window)


# In[9]:


assert "Your Surveys" not in driver.title
driver.find_elements_by_css_selector('#_ctl0_cphContent_grd1_DXPagerTop_DDB')[0].click()


# In[10]:


driver.find_elements_by_css_selector('#_ctl0_cphContent_grd1_DXPagerTop_PSP_DXI4_T > span')[0].click() # 200 items in one page


# In[11]:


columns = [name.text for name in driver.find_elements_by_css_selector('#_ctl0_cphContent_grd1_DXMainTable > tbody > tr')[1].find_elements_by_css_selector('td') if name.text.strip()]
df = pd.DataFrame(columns=columns)


# In[12]:


page_num = 0
table = []
cnt = 0
num_per_page = 200

while True:
    try:
        time.sleep(3)
        while (cnt - page_num * num_per_page < num_per_page):
            apd = [column.text for column in driver.find_elements_by_css_selector("#_ctl0_cphContent_grd1_DXDataRow"+str(cnt)+" > td")]
            if len(apd)==25:
                table.append(apd)
                cnt +=1
        driver.find_elements_by_css_selector('#_ctl0_cphContent_grd1_DXPagerTop > a[aria-label="Next"]')[0].click()
        page_num += 1
            
    except IndexError:
        print("no more page")
        break
        
    df = df.append(pd.DataFrame(table, columns=columns), ignore_index=True)
    print("finish page:", page_num, ": ", df.shape[0])
    
    table = []


# In[ ]:


driver.close()


# In[13]:


df.shape[0]


# In[14]:


df.to_csv(r"C:\Users\Jeffy\OneDrive\_Python\Project\selenium\courseevl_v2.csv", index=False)

