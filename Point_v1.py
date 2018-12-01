import pandas as pd
from pathlib import Path

import glassdoor
import heinz_course_api
import smartevals

import geo_ds
import geo_consultant
import geo_sde

import us_rent_clean
import download

"""
this is the main function
"""

CONSULTING_FILE = "data/consulting.csv"
SDE_FILE = "data/sde.csv"
DS_FILE = "data/ds.csv"
COURSE_EVL_FILE = "data/course_evl.csv"
COURSE_INFO_FILE = "data/course_info.csv"
SDE_LOC_FILE = "data/geo_sde.csv"
DS_LOC_FILE = "data/geo_ds.csv"
CONSULTANT_LOC_FILE = "data/geo_consultants.csv"
US_RENT_FILE = "data/united-states.csv"


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
    def __init__(self, consulting_file, sde_file, ds_file, course_evl_file, course_info_file, SDE_LOC_FILE,DS_LOC_FILE,CONSULTANT_LOC_FILE,US_RENT_FILE):
        self.consulting_df = pd.read_csv(consulting_file)
        self.sde_df = pd.read_csv(sde_file)
        self.ds_df = pd.read_csv(ds_file)
        self.course_evl_df = pd.read_csv(course_evl_file)
        self.course_info_df = pd.read_csv(course_info_file)
       
        self.sde_loc_df = geo_clean(SDE_LOC_FILE)
        self.ds_loc_df= geo_clean(DS_LOC_FILE)
        self.consultant_loc_df = geo_clean(CONSULTANT_LOC_FILE)
        self.rent_df = rent_clean(US_RENT_FILE)

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
        elif file == SDE_LOC_FILE:
            geo_sde()
        elif file == DS_LOC_FILE:
            geo_ds()
        elif file == CONSULTANT_LOC_FILE:
            geo_consultant()
        elif file == US_RENT_FILE:
            us_rent()



    def clean(self):
        # course datas clean and merge, new files stored automatically
        # read data from crawled files, put filename into descfile and evlfile
        def CourseClean_Merge(descfile, evlfile):
            fd = pd.read_csv(descfile)
            fd_cleaned = fd
            for i in range(len(fd)):
                fd_cleaned['course_id'][i] =  (fd['course_id'][i])[0:2] + (fd['course_id'][i])[3:]
                fd_cleaned['units'][i] = fd['units'][i][7:]
                fd_cleaned['description'][i] = fd['description'][i][12:]
            # store cleaned course description file
            fd_cleaned.to_csv('coursedesc_cleaned.csv',index=False)
            fe = pd.read_csv(evlfile)
            fe_cleaned = fe.copy()
            del fe_cleaned['Hrs Per Week 8']
            del fe_cleaned['Interest in student learning']
            del fe_cleaned['Clearly explain course requirements']
            del fe_cleaned['Clear learning objectives & goals']
            del fe_cleaned['Instructor provides feedback to students to improve']
            del fe_cleaned['Demonstrate importance of subject matter']
            del fe_cleaned['Explains subject matter of course']
            del fe_cleaned['Show respect for all students']
            del fe_cleaned['Possible Respondents']
            del fe_cleaned['Num Respondents']
            del fe_cleaned['Response Rate %']
            del fe_cleaned['Hrs Per Week 5']
            fe_cleaned = fe_cleaned[fe_cleaned['Level'] == 'Graduate']
            # store cleaned course evaluation file
            fe_cleaned.to_csv('courseevl_cleaned.csv',index=False)
            ftemp1 = fe.groupby('Course ID')['Overall course rate'].mean()
            ftemp2 = pd.DataFrame(ftemp1).reset_index()
            f_merged = pd.merge(fd_cleaned,ftemp2,left_on="course_id",right_on= "Course ID")
            f_merged.to_csv('course_merged.csv')


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

    def hist_salary(self, career):
        # TODO(zhangyu)
        if career == 'Data Scientist':
            salary_ds = ds.loc[:,['salary_low','salary_high']]
            ds['avg_salary'] = salary_ds.mean(axis=1)
            boot_ds = ds['avg_salary'].sample(frac=10, replace=True)
            filter_salary_ds = ds['avg_salary'][ds['avg_salary']<200000]
            fig, ax = plt.subplots()
            filter_salary_ds.plot.kde(ax=ax, legend=False, title='Salary for Data Scientist')
            filter_salary_ds.plot.hist(density=True, ax=ax)
            ax.set_ylabel('Probability')
            ax.grid(axis='y')
            ax.set_facecolor('#d8dcd6')
        if career == 'Software Engineer Developer':
            salary_sde = ds.loc[:,['salary_low','salary_high']]
            sde['avg_salary'] = salary_ds.mean(axis=1)
            boot_sde = ds['avg_salary'].sample(frac=10, replace=True)
            fig, ax = plt.subplots()
            boot_sde.plot.kde(ax=ax, legend=False, title='Salary for Software Engineer')
            boot_sde.plot.hist(density=True, ax=ax)
            ax.set_ylabel('Probability')
            ax.grid(axis='y')
            ax.set_facecolor('#d8dcd6')
        if career == 'Consultant':
            salary_con = ds.loc[:,['salary_low','salary_high']]
            con['avg_salary'] = salary_ds.mean(axis=1)
            boot_con = ds['avg_salary'].sample(frac=10, replace=True)
            filter_salary_con = con['avg_salary'][con['avg_salary']<150000]            
            fig, ax = plt.subplots()
            filter_salary_con.plot.kde(ax=ax, legend=False, title='Salary for Consultant')
            filter_salary_con.plot.hist(density=True, ax=ax)
            ax.set_ylabel('Probability')
            ax.grid(axis='y')
            ax.set_facecolor('#d8dcd6')
    
    def hist_review(self, career):
        #yuxin
        if career == 'Data Scientist':
            fig, ax = plt.subplots()
            ds['company_review'].plot.kde(ax=ax, legend=False, title='Company Review Score for Data Scientist')
            ds['company_review'].plot.hist(density=True, ax=ax, color = 'skyblue')
            ax.set_ylabel('Probability')
            ax.grid(axis='y')
            ax.set_facecolor('#d8dcd6')
        if career == 'Software Engineer Developer':
            fig, ax = plt.subplots()
            sde['company_review'].plot.kde(ax=ax, legend=False, title='Company Review Score for Software Engineer')
            sde['company_review'].plot.hist(density=True, ax=ax,color = 'skyblue')
            ax.set_ylabel('Probability')
            ax.grid(axis='y')
            ax.set_facecolor('#d8dcd6')
        if career == 'Consultant':
            fig, ax = plt.subplots()
            con['company_review'].plot.kde(ax=ax, legend=False, title='Company Review Score for Consultants')
            con['company_review'].plot.hist(density=True, ax=ax,color = 'skyblue')
            ax.set_ylabel('Probability')
            ax.grid(axis='y')
            ax.set_facecolor('#d8dcd6')
     
    def job_wc(self, career):
        #yuxin
        if career == 'Data Scientist':
            your_list = []
            for i in ds['description']:
                your_list.append(i + ' ')
            s = ''.join(your_list)
            stopwords= set(STOPWORDS)
            #append new words to the stopwords list
            new_words =['experience','entry', 'level','position','work','Job','will','required','requirement','team','project','provide','knowledge']
            new_stopwords=stopwords.union(new_words)
            wc = WordCloud(background_color="white", 
               width=800, height=600, margin=2,
               stopwords=new_stopwords
               )
            wc.generate(s)
            plt.figure(figsize=(10,10))
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
        
        if career == 'Software Engineer Developer':
            your_list = []
            #set the stopwords list
            stopwords= set(STOPWORDS)
            #append new words to the stopwords list
            new_words =['experience','entry', 'level','position','work','Job','will','required','requirement','team','project','provide','knowledge','Jobs']
            new_stopwords=stopwords.union(new_words)
            
            for i in sde['description']:
                your_list.append(i + ' ')
            s = ''.join(your_list)
            wc = WordCloud(background_color="white", 
                           width=800, height=600, margin=2,
                           stopwords=new_stopwords
                           )
            wc.generate(s)
            plt.figure(figsize=(10,10))
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            #Show the wordcloud
            plt.show()
   
        if career == 'Consultant':
        
            your_list = []
            #set the stopwords list
            stopwords= set(STOPWORDS)

            #append new words to the stopwords list
            new_words =['experience','entry', 'level','position','work','Job','will','required','requirement','team','project','provide','knowledge','Jobs']
            new_stopwords=stopwords.union(new_words)

            for i in con['description']:
                your_list.append(i + ' ')
            s = ''.join(your_list)
            wc = WordCloud(background_color="white", 
                           width=800, height=600, margin=2,
                           stopwords=new_stopwords
                           )
            wc.generate(s)
            plt.figure(figsize=(10,10))
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")

            #Show the wordcloud
            plt.show()

    def hotmap(self, career):
        if career == 'Data Scientist':
            job_map(ds_loc_df)
        elif career == 'Software Engineer Developer':
            job_map(sde_loc_df)
        elif career == 'Consultant':
            job_map(consultant_loc_df)
        rent_map(rent_df)


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
    data.hist_salary(person.career)
    data.hist_review(person.career)
    data.job_wc(person.career)        
    data.hotmap(person.career)




