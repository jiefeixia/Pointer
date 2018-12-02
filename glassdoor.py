from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options

MAX_PAGE = 10  # max crawling page


def crawl(file, job, level="entrylevel"):
    # job type
    start_url = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=" + job + "&jobType=" + level

    names = []
    companies = []
    company_reviews = []
    locations = []
    est_salaries = []
    descriptions = []

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(start_url)

    cnt = 0
    total = pd.DataFrame()
    for i in range(0, MAX_PAGE):
        for job in driver.find_elements_by_css_selector('#MainCol > div > ul > li'):
            try:
                job.click()
                time.sleep(3)
            except WebDriverException:
                driver.find_elements_by_css_selector(
                    "#JAModal > div > div.prettyEmail.modalContents > div.xBtn")[0].click()
                print("successfully close popup")

            try:
                name = driver.find_elements_by_css_selector("#HeroHeaderModule > div.empWrapper > div.header > h1")[
                    0].text
                company = driver.find_elements_by_css_selector(
                    "#HeroHeaderModule > div.empWrapper > div.compInfo > a")[0].text
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

                names.append(name)
                companies.append(company)
                company_reviews.append(company_review)
                est_salaries.append(est_salary)
                locations.append(location)
                descriptions.append(description)

                cnt += 1
                print("finish crawling", cnt)

            except StaleElementReferenceException:
                print("StaleElementReferenceException, Pass")
                pass
            except IndexError:
                driver.find_elements_by_css_selector("#JAModal > div > div.prettyEmail.modalContents > div.xBtn")[
                    0].click()  # close popup
                print("successfully close popup")

        driver.find_element_by_css_selector("#FooterPageNav > div > ul > li.next > a").click()
        print("finish page ", i)

        page = pd.DataFrame({"name": names, "company": companies, "company_review": company_reviews,
                             "est_salary": est_salaries, "location": locations, "description": descriptions})

        # clean
        page['company_review'] = page['company_review'].replace('★', '', regex=True)
        page['company_review'].fillna("", inplace=True)
        page['est_salary'].fillna("", inplace=True)
        salary_range = page['est_salary'].str.split("-", n=1, expand=True)
        page['salary_low'] = salary_range[0].map(min_salary)
        page['salary_high'] = salary_range[1].map(max_salary)

        # save
        page.to_csv(file, index=False, mode="a", header=False)
        total = total.append(page, ignore_index=True)

        names.clear()
        companies.clear()
        company_reviews.clear()
        locations.clear()
        est_salaries.clear()
        descriptions.clear()
        print("save item: ", cnt)

    driver.close()


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
