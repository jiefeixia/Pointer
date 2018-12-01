import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import plotly.graph_objs as go
from plotly.offline import iplot

import glassdoor
import heinz_course_api
import smartevals
import geo
import rent

"""
this is the main function
"""

CONSULTING_FILE = "data/consulting.csv"
SDE_FILE = "data/sde.csv"
DS_FILE = "data/ds.csv"
COURSE_EVL_FILE = "data/course_evl.csv"
COURSE_INFO_FILE = "data/course_info.csv"
COMPANY_LOC_FILE = "data/company_loc.csv"
RENT_FILE = "data/rent_price.csv"


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
    def __init__(self, consulting_file, sde_file, ds_file, course_evl_file, course_info_file, company_loc_file,
                 rent_file):
        self.consulting_df = pd.read_csv(consulting_file)
        self.sde_df = pd.read_csv(sde_file)
        self.ds_df = pd.read_csv(ds_file)

        course_evl_df = pd.read_csv(course_evl_file)
        course_info_df = pd.read_csv(course_info_file)

        course_evl_df = course_evl_df.drop(
            ['Hrs Per Week 8', 'Interest in student learning', 'Clearly explain course requirements',
             'Clear learning objectives & goals', 'Instructor provides feedback to students to improve',
             'Demonstrate importance of subject matter', 'Explains subject matter of course',
             'Show respect for all students', 'Possible Respondents', 'Num Respondents',
             'Response Rate %', 'Hrs Per Week 5'], axis=1)

        course_evl_df = course_evl_df[course_evl_df['Level'] == 'Graduate']

        course_evl_combine_df = pd.DataFrame(
            course_evl_df.groupby('Course ID')['Overall course rate'].mean()).reset_index()

        self.course_df = course_evl_combine_df.merge(course_info_df, how="outer", left_on="Course ID",
                                                     right_on="course_id")
        self.company_loc_df = pd.read_csv(company_loc_file)
        self.rent_df = pd.read_csv(rent_file)

    @staticmethod
    def update(filename):
        if filename == CONSULTING_FILE:
            glassdoor.crawl(file, "consultant", "entrylevel")
        elif filename == SDE_FILE:
            glassdoor.crawl(file, "software engineer", "entrylevel")
        elif filename == DS_FILE:
            glassdoor.crawl(file, "data scientist", "entrylevel")
        elif filename == COURSE_EVL_FILE:
            heinz_course_api.crawl(file)
        elif filename == COURSE_INFO_FILE:
            print("We need your andrew ID and password to log in smartevls.com to get course evaluation data")
            smartevals.crawl(file, input("Please enter your andrew ID:"), input("Please enter your password"))
        elif filename == COMPANY_LOC_FILE:
            geo.crawl(COMPANY_LOC_FILE)
        elif filename == RENT_FILE:
            rent.download(file)

    def hist_salary(self, career):
        if career == "data scientist":
            df = self.ds_df
        elif career == 'software engineer developer':
            df = self.sde_df
        else:  # career == 'consultant'
            df = self.consulting_df

        salary_ds = df.loc[:, ['salary_low', 'salary_high']]
        df['avg_salary'] = salary_ds.mean(axis=1)
        boot_df = df['avg_salary'].sample(frac=10, replace=True)
        filter_salary_ds = boot_df[np.abs(boot_df['avg_salary'] - boot_df['avg_salary'].mean())
                                   <= (3 * boot_df['avg_salary'].std())]
        fig, ax = plt.subplots()
        filter_salary_ds.plot.kde(ax=ax, legend=False, title='Salary for Data Scientist')
        filter_salary_ds.plot.hist(density=True, ax=ax)
        ax.set_ylabel('Probability')
        ax.grid(axis='y')
        ax.set_facecolor('#d8dcd6')

    def hist_review(self, career):
        if career == "data scientist":
            df = self.ds_df
        elif career == 'software engineer developer':
            df = self.sde_df
        else:  # career == 'consultant':
            df = self.consulting_df

        fig, ax = plt.subplots()
        df['company_review'].plot.kde(ax=ax, legend=False, title='Company Review Score for Data Scientist')
        df['company_review'].plot.hist(density=True, ax=ax, color='skyblue')
        ax.set_ylabel('Probability')
        ax.grid(axis='y')
        ax.set_facecolor('#d8dcd6')

    def job_wc(self, career):
        if career == "data scientist":
            df = self.ds_df
        elif career == 'software engineer developer':
            df = self.sde_df
        else:  # career == 'consultant':
            df = self.consulting_df

        your_list = []
        for i in df['description']:
            your_list.append(i + ' ')
        s = ''.join(your_list)
        stopwords = set(STOPWORDS)
        # append new words to the stopwords list
        new_words = ['experience', 'entry', 'level', 'position', 'work', 'Job', 'will', 'required', 'requirement',
                     'team', 'project', 'provide', 'knowledge']
        new_stopwords = stopwords.union(new_words)
        wc = WordCloud(background_color="white",
                       width=800, height=600, margin=2,
                       stopwords=new_stopwords
                       )
        wc.generate(s)
        plt.figure(figsize=(10, 10))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")

    def heat_map(self, career):
        if career == 'data scientist':
            df = self.ds_df
        elif career == 'software engineer developer':
            df = self.sde_df
        else:  # career == 'consultant':
            df = self.consulting_df

        dat = dict(type='choropleth',
                   colorscale='Viridis',
                   locations=df['state'],
                   z=df['cnt'],
                   locationmode='USA-states',
                   marker=dict(line=dict(color='rgb(255,255,255)', width=2)),
                   colorbar={'title': "Count of jobs"}
                   )
        layout = dict(title='Consultant Job Distribution around US',
                      geo=dict(scope='usa',
                               showlakes=True))

        choromap = go.Figure(data=[dat], layout=layout)
        iplot(choromap, validate=False)

    def rent_map(self):
        map_data = dict(type='choropleth',
                    colorscale='Viridis',
                    reversescale=True,
                    locations=self.rent_df['state'],
                    z=self.rent_df['rent'],
                    locationmode='USA-states',
                    text=self.rent_df['Region Name'],
                    marker=dict(line=dict(color='rgb(255,255,255)', width=1)),
                    colorbar={'title': "Rent(yearly)"})
        layout = dict(title='Rent Distribution around US',
                      geo=dict(scope='usa',
                               showlakes=True))

        choromap = go.Figure(data=[map_data], layout=layout)
        iplot(choromap, validate=False)


if __name__ == "__main__":
    # TODO some fancy welcome message

    # instantiate Data
    # check if exist
    files_list = [CONSULTING_FILE, SDE_FILE, DS_FILE, COURSE_EVL_FILE, COURSE_INFO_FILE, COMPANY_LOC_FILE, RENT_FILE]
    for file in files_list:
        if not Path(file).is_file():
            Data.update(file)

    data = Data(*files_list)

    # instantiate Person
    person = Person(input("Please enter your career:").lower, input("Please enter your location:").lower)

    # recommend
    person.recommend_job()
    person.recommend_course()
    data.hist_salary(person.career)
    data.hist_review(person.career)
    data.job_wc(person.career)
    data.heat_map(person.career)
