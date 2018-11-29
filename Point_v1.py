import pandas as pd
from pathlib import Path

import glassdoor
import heinz_course_api
import smartevals

"""
this is the main function
"""

CONSULTING_FILE = "data/consulting.csv"
SDE_FILE = "data/sde.csv"
DS_FILE = "data/ds.csv"
COURSE_EVL_FILE = "data/course_evl.csv"
COURSE_INFO_FILE = "data/course_info.csv"
COMPANY_LOC_FILE = "data/company_loc.csv"


class Person:
    def __init__(self, career, location=None):
        self.career = career
        self.location = location

    def recommend_course(self, jobs_df, courses_df):
        # TODO(liwei)
        pass

    def recommend_job(self, jobs_df):
        pass


class Data:
    def __init__(self, consulting_file, sde_file, ds_file, course_evl_file, course_info_file, company_loc_file):
        self.consulting_df = pd.read_csv(consulting_file)
        self.sde_df = pd.read_csv(sde_file)
        self.ds_df = pd.read_csv(ds_file)
        self.course_evl_df = pd.read_csv(course_evl_file)
        self.course_info_df = pd.read_csv(course_info_file)
        # TODO(xinyi) combine two course df
        self.company_loc_df = pd.read_csv(company_loc_file)

    @staticmethod
    def update(self, file):
        if file == CONSULTING_FILE:
            glassdoor.crawl(file, "consultant", "entrylevel")
        elif file == SDE_FILE:
            glassdoor.crawl(file, "software engineer", "entrylevel")
        elif file == DS_FILE:
            glassdoor.crawl(file, "data scientist", "entrylevel")
        elif file == COURSE_EVL_FILE:
            heinz_course_api.crawl(file)
        elif file == COURSE_INFO_FILE:
            print("We need your andrew ID and password to log in smartevls.com to get course evaluation data")
            smartevals.crawl(file, input("Please enter your andrew ID:"), input("Please enter your password"))
        elif file == COMPANY_LOC_FILE:
            # TODO(xinyi)
            pass

    def clean(self):
        # TODO(summer)
        def cleanData(inFileName,outFileName):
            ds = pd.read_csv(inFileName)
            ds['company_review'] = ds['company_review'].replace('★','', regex=True)
            ds['company_review'].fillna("", inplace=True)
            ds['est_salary'].fillna("",inplace=True)
            salaryRange = ds['est_salary'].str.split("-", n = 1, expand = True)

        def minSalary(amount):
            if amount.endswith("k"):
                if amount.startswith("Employer Provided Salary:$"):
                    return int(amount[len("Employer Provided Salary:$"):-1])*1000
                else:
                    return int(amount[1:-1])*1000
            elif amount.startswith("Employer Provided Salary:$"):
                return int(amount[amount.rfind("$")+1:])*8*40*52
            elif amount[1:].isnumeric():
                return int(amount[1:])*8*40*52
            else:
                return amount

        def maxSalary(amount):
            if amount == None:
                return ""
            elif amount.endswith("k(Glassdoor est.)") or amount.endswith("k(Employer est.)") :
                pos = amount.find("k")
                return int(amount[1:pos])*1000
            elif amount.endswith("Per Hour(Glassdoor est.)"):
                pos = amount.find("Per")
                return int(amount[1:pos])*8*40*52
            elif amount.endswith("k") and amount.startswith("$"):
                return int(amount[1:-1])*1000
            elif amount.endswith("Per Hour"):
                return int(amount[1:amount.find("Per Hour")])*8*40*52
            else:
                return amount
       
        ds['salary_low'] = salaryRange[0].map(minSalary)
        ds['salary_high'] = salaryRange[1].map(maxSalary)
        ds.loc[:,['name', 'company', 'company_review', 'salary_low', 'salary_high', 'location','description']].to_csv(outFileName)
    cleanData("data/consulting.csv","consultant_cleaned.csv")
    cleanData("data/sde.csv","sde_cleaned.csv")
    cleanData("data/ds.csv","ds_cleaned.csv")

    def hist(self, job):
        # TODO(zhangyu)
        pass

    def hotmap(self, job):
        # TODO(xinyi)
        pass


if __name__ == "__main__":
    # TODO some fancy welcome message

    # instantiate Data
    # check if exist
    files_list = [CONSULTING_FILE, SDE_FILE, DS_FILE, COURSE_EVL_FILE, COURSE_INFO_FILE, COMPANY_LOC_FILE]
    for file in files_list:
        if not Path(file).is_file():
            Data.update(file)
    data = Data(file for file in files_list)

    # instantiate Person
    person = Person(input("Please enter your career:"), input("Please enter your location:"))

    # recommend
    person.recommend_job()
    person.recommend_course()
    data.hist(person.career)
    data.hotmap(person.career)




