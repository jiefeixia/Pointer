from selenium import webdriver
from selenium.common.exceptions import WebDriverException, ElementNotVisibleException, StaleElementReferenceException
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool
import os
from functools import partial
import re


"""
This module is used to crawl the job information from https://www.glassdoor.com. 
The job information includes job name, working location, company name, company review rating, 
salary estimated by glassdoor, job description. 
We will extract the qualification from job description for future text mining usage.

Its crawl() method is called by the main module.
Because the loading speed is slow, we use a multi-threading strategy in this method. It will create several
(your CPU core numbers -1) processes to call crawl_page() function. 

After finished, it will store the file into file(which is its argument).
"""


MAX_PAGE = 3  # default max crawling page
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


def crawl(file, job, level="entrylevel", max_page=MAX_PAGE):
    with Pool(os.cpu_count()) as p:
        partial_crawl_page = partial(crawl_page, job=job, level=level)
        page_list = p.map(partial_crawl_page, [page_num for page_num in range(1, max_page + 1)])

    total = pd.DataFrame()
    for page_df in page_list:
        total = total.append(page_df, ignore_index=True)

    print("Save " + str(total.shape[0]) + " items about " + job)
    total.to_csv(file, index=False)


# single thread function
def crawl_page(page_num, job, level="entrylevel", chrome_headless=False):
    start_url = "https://www.glassdoor.com/Job/" + job.replace(" ", "-") + "-jobs-SRCH_KO0," + \
                str(len(job.replace(" ", "-"))) + "_IP" + str(page_num) + ".htm?jobType=" + level

    if chrome_headless:  # show chrome GUI when in debug mode
        driver = webdriver.Chrome()
    else:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

    driver.get(start_url)

    names = []
    companies = []
    company_reviews = []
    locations = []
    est_salaries = []
    descriptions = []
    qualifications = []

    cnt = 0

    for job in driver.find_elements_by_css_selector('#MainCol > div > ul > li'):
        try:
            job.click()
            time.sleep(3)
        except WebDriverException:
            driver.find_elements_by_css_selector(
                "#JAModal > div > div.prettyEmail.modalContents > div.xBtn")[0].click()
            print("successfully close popup")

        try:
            name = driver.find_elements_by_css_selector("#HeroHeaderModule > div.empWrapper > div.header > h1")[0].text
        except IndexError:
            try:  # in case pop up
                driver.find_elements_by_css_selector("#JAModal > div > div.prettyEmail.modalContents > div.xBtn")[
                    0].click()  # close popup
                print("successfully close popup")
            except ElementNotVisibleException:  # in case name selector change
                name = driver.find_elements_by_css_selector(
                    "#HeroHeaderModule > div.empWrapper.ctasTest > div.empInfo > div.header > h1")[0].text
        except StaleElementReferenceException:  # need to update element
            print("StaleElementReferenceException, Pass")
            pass

        finally:
            try:
                company = driver.find_elements_by_css_selector(
                    "#HeroHeaderModule > div.empWrapper > div.compInfo > a")[0].text
            except IndexError:
                company = None
                pass
            try:
                company_review = \
                    driver.find_elements_by_css_selector("div.compInfo > span.compactRating.lg.margRtSm")[0].text

            except IndexError:
                company_review = None
                pass
            try:
                est_salary = driver.find_elements_by_css_selector("div.salaryRow > div > span")[0].text
            except IndexError:
                est_salary = None
                pass
            try:
                location = driver.find_elements_by_css_selector(
                    "#HeroHeaderModule > div.empWrapper > div.compInfo > span:nth-child(3)")[0].text
            except IndexError:
                location = None
                pass
            description = driver.find_elements_by_css_selector("#JobDescriptionContainer")[0].text

            # find qualification in the description
            qualification = None  # default not found
            # assume qualification start with first qualification(s):/requirement(s):
            start_pos_list = list(re.finditer("(qualification|requirement).{,3}:", description, re.IGNORECASE))
            if len(start_pos_list) > 0:
                start = start_pos_list[0].span()[1]
                # assume qualification end with empty lines
                end = len(description) - 1  # default to end
                for match in re.finditer("(qualification|requirement).{,3}:", description, re.IGNORECASE):
                    if match.span()[1] > start:  # first empty line appear after start position
                        end = match.span()[1]
                        break
                qualification = description[start:end]


            names.append(name)
            companies.append(company)
            company_reviews.append(company_review)
            est_salaries.append(est_salary)
            locations.append(location)
            descriptions.append(description)
            qualifications.append(qualification)

            cnt += 1
            print("finish crawling item ", cnt, " on page ", page_num)

    driver.close()

    page = pd.DataFrame({"name": names, "company": companies, "company_review": company_reviews,
                         "est_salary": est_salaries, "location": locations, "description": descriptions,
                        "qualification": qualifications})

    # clean
    page['company_review'] = page['company_review'].replace('★', '', regex=True)
    page['company_review'].fillna("", inplace=True)
    page['est_salary'].fillna("", inplace=True)
    salary_range = page['est_salary'].astype(str).str.split("-", n=1, expand=True)
    page['salary_low'] = salary_range[0].map(min_salary)
    page['salary_high'] = salary_range[1].map(max_salary)

    page["state"] = page["location"].apply(find_state)

    page = page.drop("est_salary", axis=1)

    names.clear()
    companies.clear()
    company_reviews.clear()
    locations.clear()
    est_salaries.clear()
    descriptions.clear()

    print("finish page ", page_num)
    return page


def min_salary(amount):
    if amount.endswith("k"):
        if amount.startswith("Employer Provided Salary:$"):
            return int(amount[len("Employer Provided Salary:$"):-1]) * 1000
        else:
            return int(amount[1:-1]) * 1000
    elif amount.startswith("Employer Provided Salary:$"):
        return int(amount[amount.rfind("$") + 1:]) * 8 * 40 * 52
    elif amount[1:].isnumeric():
        return int(amount[1:]) * 8 * 40 * 52
    else:
        return amount


def max_salary(amount):
    if not amount:
        return ""
    elif amount.endswith("k(Glassdoor est.)") or amount.endswith("k(Employer est.)"):
        pos = amount.find("k")
        return int(amount[1:pos]) * 1000
    elif amount.endswith("Per Hour(Glassdoor est.)"):
        pos = amount.find("Per")
        return int(amount[1:pos]) * 8 * 40 * 52
    elif amount.endswith("k") and amount.startswith("$"):
        return int(amount[1:-1]) * 1000
    elif amount.endswith("Per Hour"):
        return int(amount[1:amount.find("Per Hour")]) * 8 * 40 * 52
    else:
        return amount


# find state on location info to draw heat map
def find_state(loc):
    for key in us_state_abbrev.keys():
        if key in str(loc):
            return us_state_abbrev[key]
        elif us_state_abbrev[key] in str(loc):
            return us_state_abbrev[key]


# for test purpose
if __name__ == "__main__":
    # crawl("data/test.csv", "software engineer", max_page=1)
    crawl_page(20, "consultant", chrome_headless=True)
