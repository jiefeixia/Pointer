# :point_right: Pointer
This program is the Course project for Data Focus Python. It can pave the way to your successful career!

## Instruction([video](https://youtu.be/m8LF65Qc5Cw))
First, the program will check whether all necessary data file exists. If not, it will automatically download the missing data.  
Then it will come to the main menu. You can choose the following functions:  
1. Summary statistics for three tracks:
    * Salary Histogram
    * Company Review Histogram
    * WordCloud for Job Description
    * Job numbers heat map
    * Rent price heat map
2. Choose a specific career:
    * Show recommended Course (enter optional skills you particularly want to learn):
        * Course ID 
        * Course Name
        * Course Overall Evaluation Score    
    * Show Recommended Job (enter optional preferred location):
        * Job Name
        * Company Name
        * Average Salary
        * Location
3. Update and clean
    * Crawl job data from [Glassdoor](https://www.glassdoor.com)
        * ds.csv
        * sde.csv
        * consultant.csv
    * Crawl course evaluation data from [cmu course evaluation](https://www.smartevl.com)
        * course_evl.csv
    * Crawl course information data from [heinz course API](https://api.heinz.cmu.edu/courses_api)
        * course_info.csv
    * Download rent price data from [Zillow](https://www.zillow.com/home-values/) and convert it into .csv file
        * rent_price.csv
    * Get data from [arcgis API](https://www.arcgis.com/index.html)
        * company_loc.csv
        
## Highlight Function
* The multi-threading strategy is used to speed up when crawling from a dynamic website.
* Most crawl module uses [selenium](https://www.seleniumhq.org/) and  [chrome driver](http://chromedriver.chromium.org/)  in case the website is built on AJAX.
* The recommendation function is based on [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) algorithm to increase its precision.
* The program can update its database by its inside method, so after the course finishing, you can still use this program.
* Some of its job insight graphs is interactive.  

## Installation
* Download the whole folder and decompression
* Required environment: python 3.5+
* Required packages: `requirements.txt`. You can install by `pip install -r requirements.txt`  
  You need to download the [chrome driver](http://chromedriver.chromium.org/downloads) and add its path to your environment variable for selenium.
* If you are using Anaconda, don't forget to activate your environment by `activate env_name`(you can find your environment name by `conda env list`). Or you might see the error  
```
Drawing XXX graph
This application failed to start because it could not find or load the Qt platform plugin "windows"
in "".

Available platform plugins are: direct2d, minimal, offscreen, windows.

Reinstalling the application may fix this problem.
```

## Run

* run Point_v1.py

 
