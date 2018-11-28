from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
import time
import pandas as pd


MAX_PAGE = 10  # max crawling page


def crawl(job, level, file):
    # job type
    start_url = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=" + job + "&jobType=" + level

    names = []
    companies = []
    company_reviews = []
    locations = []
    est_salaries = []
    descriptions = []

    columns = ["name", "company", "company_review", "est_salary", "location", "description"]
    df = pd.DataFrame(columns=columns)
    df.to_csv(file, index=False)

    driver = webdriver.Chrome()
    driver.get(start_url)

    cnt = 0
    for i in range(0, MAX_PAGE):  # scrap 10 pages
        for job in driver.find_elements_by_css_selector('#MainCol > div > ul > li'):
            try:
                job.click()
            except WebDriverException:
                driver.find_elements_by_css_selector("#JAModal > div > div.prettyEmail.modalContents > div.xBtn")[0].click()  # close popup
                print("successfully close popup")

            try:
                time.sleep(3)
                name = driver.find_elements_by_css_selector("#HeroHeaderModule > div.empWrapper > div.header > h1")[
                    0].text
                company = driver.find_elements_by_css_selector("#HeroHeaderModule > div.empWrapper > div.compInfo > a")[
                    0].text
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
        pd.DataFrame(
            {0: names, 1: companies, 2: company_reviews, 3: est_salaries, 4: locations, 5: descriptions}).to_csv(
            file, index=False, mode="a", header=False)

        names.clear()
        companies.clear()
        company_reviews.clear()
        locations.clear()
        est_salaries.clear()
        descriptions.clear()
        print("save item: ", cnt)
    driver.close()
