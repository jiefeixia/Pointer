import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import plotly.graph_objs as go
import plotly
import os

import glassdoor
import heinz_course_api
import smartevals
import geo
import rent

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

"""
This is the main module to run.
There are two classes in this module: People and Data.

People class is used to create the user's profile and recommend courses and jobs based on his/her profile.
Its recommend_course method need to read corenlp_stopwords.txt as its stops words for NLP. 
It uses tf-idf algorithm to match the course with your desired job description.

Data class is used to create the database instance for this program. Each table is an instance variable 
and is stored as a Pandas DataFrame format. The program will first look at the data folder to check 
whether all files exist. If not, it will call the Data.update() method to crawl/download the data.
There are also other methods used to generate different graphs. 
"""

CONSULTING_FILE = "data/consultant.csv"
SDE_FILE = "data/sde.csv"
DS_FILE = "data/ds.csv"
COURSE_EVL_FILE = "data/course_evl.csv"
COURSE_INFO_FILE = "data/course_info.csv"
COMPANY_LOC_FILE = "data/company_loc.csv"
RENT_FILE = "data/rent_price.csv"


# test file is less than 100 item, used for debug
# CONSULTING_FILE = "data/consultant_test.csv"
# SDE_FILE = "data/sde_test.csv"
# DS_FILE = "data/ds_test.csv"


class Person:
    def __init__(self, career, location=None):
        self.career = career
        if location is not None:
            self.location = location.lower()

    def recommend_course(self, data):
        if self.career == 'data scientist':
            job = data.ds_df
        elif self.career == 'software engineer':
            job = data.sde_df
        elif self.career == 'consultant':
            job = data.consulting_df

        print("\n\n*************************" + "recommend courses of " + career + "***************************")
        desc = job["description"].tolist()

        print("calculating recommend courses")

        coursedes = list(data.course_df['description'])
        courseout = list(data.course_df['learning_outcome'])

        course = []
        for i in range(len(courseout)):
            if type(coursedes[i]) != str:
                coursedes[i] = str(coursedes[i])  # make sure data type are string
            if type(courseout[i]) != str:
                courseout[i] = str(courseout[i])  # make sure data type are string
            course.append(coursedes[i] + courseout[i])  # combine description and outcome together

        # deal with stopwords
        stop = open('corenlp_stopwords.txt', encoding='utf-8')
        st = stop.readlines()
        for i in range(len(st)):
            st[i] = st[i].strip('\n')  # delete '\n' in each word
        st.extend(
            ['allow', 'outcomes', 'some', 'mini', 'another', 'student', 'in', 'or', 'either', 'final', 'exam', 'mid',
             'by', 'areas', 'also', 'today', 'course', 'Outcomes:', 'will', 'Work', 'Students', 'The', 'It', 'us',
             'class', 'Learning', 'course,', ' ', 'try', 'on', 'results', 'how', 'what', 'he', 'she', 'courses',
             'professor', 'their', 'one', 'two', 'develop', 'problem', 'problems', 'perform', 're', 'job', 'ed', 'edu',
             'many', 'year', 'years', 'multi', 'become', 'use', 'homework', 'come', 'came', 'three', 'skills', 'art',
             'life', 'success', 'now', 'career', 'students', 'short', 'long', 'able', 'professional', 'arts', 'master',
             'across', 'field', 'target', 'using', 'cut'])
        for i in range(len(course)):
            out = ''
            for word in course[i].split(' '):
                if word not in st:
                    out = out + word + ' '
            course[i] = out

        vectorizer = CountVectorizer()  #
        transformer = TfidfTransformer()  #
        tfidf = transformer.fit_transform(vectorizer.fit_transform(course))  # calculate tf-idf
        word = vectorizer.get_feature_names()  # all words in the word bag
        weight = tfidf.toarray()  # get matrix of tf-idf
        key = []
        for i in range(len(weight)):
            t = np.argsort(-weight[i])
            s = ''
            for j in range(40):

                if word[t[j]] not in st:
                    s = s + ' ' + word[t[j]]
            key.append(s)
        count = []
        for i in range(len(key)):
            c = 0
            for word in key[i].split(' '):
                if word != '':
                    for j in desc:
                        a = j.count(word)
                        c += a

            count.append(c)
        recommended = set()
        skillsinput = input(
            "Do you have specific skills you want to learn?\nlist skills separated by ',',\nanswer 'N' if you don't.")
        if skillsinput != 'N':
            for i in range(len(key)):
                for word in skillsinput.split(','):
                    if word.lower() in key[i].lower():
                        recommended.add(
                            str(data.course_df['course_id'][i]) + ": " + "%-50s" % data.course_df['names'][i] +
                            'Course rate:' + '%.2f' % data.course_df['Overall course rate'][i])
            if len(recommended) != 0:
                print("COURSES RECOMMENDED:")
                for i in list(recommended)[0: 5 if len(recommended) > 5 else len(recommended)]:
                    print(i)
        else:
            for i in np.argsort(count)[-4:]:
                recommended.add(
                    str(data.course_df['course_id'][i]) + ": " + "%-50s" % data.course_df['names'][i] +
                    'course rate:' + '%.2f' % data.course_df['Overall course rate'][i])
            print("COURSES RECOMMENDED:")
            for i in recommended:
                print(i)
        pass

    def recommend_job(self, data):
        if self.career == 'data scientist':
            job = data.ds_df
        elif self.career == 'software engineer':
            job = data.sde_df
        elif self.career == 'consultant':
            job = data.consulting_df

        print("*******************" + "recommend jobs of " + career + "*******************\n")

        if self.location is not None:
            job['location'] = job['location'].str.lower()
            recommend_job = job[job['location'].str.contains(self.location).fillna(False).values]
        else:
            recommend_job = job

        recommend_job = recommend_job.sort_values(by="company_review", ascending=False)
        recommend_job["avg_salary"] = (recommend_job["salary_low"] + recommend_job["salary_low"]) / 2
        recommend_job = recommend_job.reset_index(drop=True)

        if len(recommend_job) == 0:
            print("not job found on your preferred location")
        else:
            for i in range(10 if len(recommend_job) > 10 else len(recommend_job)):
                print(str(i) + ". " + "%-20s" % recommend_job.loc[i, "name"] +
                      " Company: " + "%-10s" % recommend_job.loc[i, "company"] +
                      "(%.2f" % recommend_job.loc[i, "company_review"] + ")" +
                      " Est salary: %.2f" % recommend_job.loc[i, "avg_salary"] +
                      " Location: " + recommend_job.loc[i, "location"])


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

        self.course_df = course_evl_combine_df.merge(course_info_df, how="inner", left_on="Course ID",
                                                     right_on="course_id")
        self.company_loc_df = pd.read_csv(company_loc_file)
        self.rent_df = pd.read_csv(rent_file)

    @staticmethod
    def update(filename):
        print("Updating " + filename)
        if filename == CONSULTING_FILE:
            glassdoor.crawl(file, "consultant", "entrylevel", max_page=19)
        elif filename == SDE_FILE:
            glassdoor.crawl(file, "software engineer", "entrylevel", max_page=29)
        elif filename == DS_FILE:
            glassdoor.crawl(file, "data scientist", "entrylevel", max_page=10)
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

        print("Drawing salary histogram for " + career + "(predicted by glassdoor)")

        df = df.loc[:, ["name", 'salary_low', 'salary_high']]
        df['avg_salary'] = df.mean(axis=1)
        boot_df = df['avg_salary'].sample(frac=10, replace=True)  # bootstrap to increase sample
        boot_df = boot_df[np.abs(boot_df - boot_df.mean()) <= (3 * boot_df.std())]  # remove outlier (>3sigma)
        fig, ax = plt.subplots()
        boot_df.plot.kde(ax=ax, legend=False, title='Salary for ' + career)
        boot_df.plot.hist(density=True, ax=ax)
        ax.grid(axis='y')
        ax.set_facecolor('#d8dcd6')

        img_path = career + "hist_salary.png"
        plt.savefig(img_path)
        print("salary histogram for " + career + " saved in " + os.getcwd().split()[0] + img_path)

    def hist_review(self, career):
        if career == "data scientist":
            df = self.ds_df
        elif career == 'software engineer':
            df = self.sde_df
        else:  # career == 'consultant':
            df = self.consulting_df

        print("Drawing company review histogram for " + career)

        fig, ax = plt.subplots()
        df['company_review'].plot.kde(ax=ax, legend=False, title='Company Review Score for ' + career)
        df['company_review'].plot.hist(density=True, ax=ax, color='skyblue')
        ax.grid(axis='y')
        ax.set_facecolor('#d8dcd6')

        img_path = career + "hist_review.png"
        plt.savefig(img_path)
        print("company review histogram for " + career + " saved in " + os.getcwd().split()[0] + img_path)

    def job_wc(self, career):
        if career == "data scientist":
            df = self.ds_df
            new_words = ['experience', 'entry', 'level', 'position', 'work', 'Job', 'will', 'required', 'requirement',
                         'team', 'project', 'provide', 'knowledge']
        elif career == 'software engineer':
            df = self.sde_df
            new_words = ['experience', 'entry', 'level', 'position', 'work', 'Job', 'will', 'required', 'requirement',
                         'team', 'project', 'provide', 'knowledge', 'Jobs']
        else:  # career == 'consultant':
            df = self.consulting_df
            new_words = ['experience', 'entry', 'level', 'position', 'work', 'Job', 'will', 'required', 'requirement',
                         'team', 'project', 'provide', 'knowledge', 'Jobs']

        print("Drawing word cloud for " + career)
        your_list = []
        for i in df['description']:
            your_list.append(i + ' ')
        s = ''.join(your_list)
        stopwords = set(STOPWORDS)

        # append new words to the stopwords list
        new_stopwords = stopwords.union(new_words)
        wc = WordCloud(background_color="white",
                       width=800, height=600, margin=2,
                       stopwords=new_stopwords
                       )
        wc.generate(s)
        plt.figure(figsize=(10, 10))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")

        img_path = career + "_word_cloud.png"
        plt.savefig(img_path)
        print("Word cloud for " + career + " saved in " + os.getcwd().split()[0] + img_path)

    def job_map(self, career):
        if career == 'data scientist':
            df = self.ds_df
        elif career == 'software engineer':
            df = self.sde_df
        else:  # career == 'consultant':
            df = self.consulting_df

        print("Drawing heat map for job numbers of " + career)

        # count job num
        df = df.dropna().groupby(['state'], as_index=False)['state'].agg({'cnt': 'count'})
        df = df.iloc[1:]
        df['cnt'] = pd.to_numeric(df['cnt']).astype(float)

        # draw map
        map_data = dict(type='choropleth',
                        colorscale='Viridis',
                        locations=df['state'],
                        z=df['cnt'],
                        locationmode='USA-states',
                        marker=dict(line=dict(color='rgb(255,255,255)', width=2)),
                        colorbar={'title': "Count of jobs"}
                        )

        layout = dict(title='Consultant Job Distribution around US',
                      geo=dict(scope='usa', showlakes=True))
        choromap = go.Figure(data=[map_data], layout=layout)

        img_path = career + '_job_map.html'
        plotly.offline.plot(choromap, filename=img_path)
        print("Job numbers heat map of " + career + " saved in: " + os.getcwd().split()[0] + img_path)

    def rent_map(self):
        print("Drawing rent price heat map")
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
        img_path = 'rent_map.html'
        plotly.offline.plot(choromap, filename=img_path)
        print("Rent price heat map saved in " + os.getcwd().split()[0] + img_path)


# to give career base on number input
def career_num():
    num = input("\n\nPlease enter the job type number:\n"
                "1. consultant\n"
                "2. software engineer\n"
                "3. data scientist\n")

    if num == "1":
        return "consultant"
    elif num == "2":
        return "software engineer"
    elif num == "3":
        return "data scientist"
    else:
        print("Cannot find your job number.")
        return None


if __name__ == "__main__":
    print("initializing program...")
    # instantiate Data
    # check if exist
    files_list = [CONSULTING_FILE, SDE_FILE, DS_FILE, COURSE_EVL_FILE, COURSE_INFO_FILE, COMPANY_LOC_FILE, RENT_FILE]
    for file in files_list:
        if not Path(file).is_file():
            print(file + " not found")
            Data.update(file)
        else:
            print(file + " founded")

    database = Data(*files_list)

    print("\n\n******************Welcome to pointer!*************************")
    run = input("please enter the number to choose functions\n"
                "1 Insights for finding your career\n"
                "2 Recommendation job and course for you\n"
                "3 Update the data\n"
                "4 Exit\n")

    while run != "4":
        if run == "1":  # generate graph
            graph_num = input("\n\nPlease enter the graph you want to save:\n"
                              "1. salary histogram\n"
                              "2. company review histogram\n"
                              "3. word cloud of job description\n"
                              "4. job number heat map\n"
                              "5. rent price heat map\n"
                              )
            try:
                graph_num = int(graph_num)
                if graph_num <= 4:
                    print("You can choose your preferred job type:\n")
                    career = career_num()
                    if career is None:
                        continue
                    if graph_num == 1:
                        database.hist_salary(career)
                    elif graph_num == 2:
                        database.hist_review(career)
                    elif graph_num == 3:
                        database.job_wc(career)
                    elif graph_num == 4:
                        database.job_map(career)
                elif graph_num == 5:
                    database.rent_map()
                else:
                    print("Cannot find your required graph")
            except ValueError:
                print("Cannot find your required graph")

        elif run == "2":  # recommend course
            career = career_num()
            if career is None:
                continue
            person = Person(career)

            sub_run = input("Please enter the recommendation type:\n"
                            "a. Course\n"
                            "b. Job\n")
            if sub_run == "a":
                person.recommend_course(database)
            elif sub_run == "b":
                person.location = input("Please enter your preferred working location:\n").lower()
                person.recommend_job(database)
            else:
                print("Cannot find your required function")
        elif run == "3":  # update data
            print("file list:")
            for idx, file in enumerate(files_list):
                print(str(idx) + ". " + file)
            file_num = input("please input the file number you want to update:\n")
            try:
                if int(file_num) in range(0,len(files_list)):
                    Data.update(files_list[int(file_num)])
                else:
                    print("Cannot find the file you want to update")
            except ValueError:
                print("Cannot find the file you want to update")
                pass

        else:  # other input number
            print("Cannot find your input function number")

        run = input("\n\n*******************Main menu************************\n"
                    "please enter the number to choose functions\n"
                    "1 Insights for finding your career\n"
                    "2 Recommendation job and course for you\n"
                    "3 Update the data\n"
                    "4 Exit\n")

    print("Good luck on finding your job, bye!")

