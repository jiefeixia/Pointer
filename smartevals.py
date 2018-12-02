import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd


def crawl(file, andrew_id, password):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.smartevals.com/SchoolList.aspx")

    driver.find_elements_by_css_selector('a.dxp-num[aria-label="Page 3 of 22"]')[0].click()

    driver.find_elements_by_xpath("//td[contains(text(), 'Carnegie Mellon University')]/..//input")[0].click()

    driver.find_elements_by_css_selector('#j_username')[0].send_keys(andrew_id)
    driver.find_elements_by_css_selector('#j_password')[0].send_keys(password)
    driver.find_elements_by_css_selector('input.loginbutton')[0].click()

    driver.find_elements_by_css_selector('#lnkSeeResultsImg')[0].click()
    table_window = driver.window_handles[1]
    driver.switch_to.window(table_window)

    assert "Your Surveys" not in driver.title
    driver.find_elements_by_css_selector('#_ctl0_cphContent_grd1_DXPagerTop_DDB')[0].click()

    driver.find_elements_by_css_selector('#_ctl0_cphContent_grd1_DXPagerTop_PSP_DXI4_T > span')[0].click()  # 200/page

    columns = [name.text for name in
               driver.find_elements_by_css_selector(
                   '#_ctl0_cphContent_grd1_DXMainTable > tbody > tr')[1].find_elements_by_css_selector('td')
               if name.text.strip()]

    page_num = 0
    table = []
    cnt = 0
    num_per_page = 200

    while True:
        try:
            time.sleep(3)
            while cnt - page_num * num_per_page < num_per_page:
                apd = [column.text for column in
                       driver.find_elements_by_css_selector("#_ctl0_cphContent_grd1_DXDataRow" + str(cnt) + " > td")]
                if len(apd) == 25:
                    table.append(apd)
                    cnt += 1

            # click next page
            driver.find_elements_by_css_selector('#_ctl0_cphContent_grd1_DXPagerTop > a[aria-label="Next"]')[0].click()
            page_num += 1

        except IndexError:
            print("no more page")
            break

        df = df.append(pd.DataFrame(table, columns=columns), ignore_index=True)
        print("finish page:", page_num, ": ", df.shape[0])

        table = []

    driver.close()

    # convert Course ID from object dtype to int
    df["Course ID"] = df["Course ID"].str.replace("-", "")
    df = df[df["Course ID"].str.isdigit()]
    df["Course ID"] = df["Course ID"].astype(int)

    df.to_csv(file, index=False)
