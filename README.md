# :point_right: Pointer
This is the Course project for Data Focus Python. You can use this program to find your desired job!

## Instruction
First the program will check whether all necessary data file exits. 
If not, it will automatically download the missing data.
If yes, it will come to the main menu. You can choose the following functions:  
1. Summary statistics for three tracks:
    * Salary Histogram
    * Company Review Histogram
    * WordCloud for Job Description
    * Job numbers heat map
    * Rent price heat map
2. Enter specific career:
    * Show recommended Course (enter optional specific skills to learn):
        * Course ID 
        * Course Name
        * Course Overall Evaluation Score    
    * Show Recommended Job (enter optional preferred location):
        * Job Name
        * Company Name
        * Average Salary
        * Location
3. Update and clean
    * Crawl job data from [glassdoor](https://www.glassdoor.com)
        * ds.csv
        * sde.csv
        * consultant.csv
    * Crawl course evaluation data from [cmu course evaluation](https://www.smartevl.com)
        * course_evl.csv
    * Crawl course information data from [heinz course API](https://api.heinz.cmu.edu/courses_api)
        * course_info.csv
    * Download rent price data from [pillow](https://www.zillow.com/home-values/) and convert it into .csv file
        * rent_price.csv
    * Get data from [arcgis API](https://www.arcgis.com/index.html)
        * company_loc.csv
        
## Highlight Function
* The multi-threading strategy is used to speed up when crawling from dynamic website.
* Most crawl module uses [selenium](https://www.seleniumhq.org/) and chrome driver in case the website is build on AJAX.
* The recommendation function is based on [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) algorithm to increase its precision.
        
## Installation
* Download the whole folder and decompression
* Required environment: python 3.5+
* Required packages: `requirement.txt`. You can install by `pip install -r requirement.txt`  
  You need to download the [chrome driver](http://chromedriver.chromium.org/downloads) and add its path to your environment variable for selenium.
* If you are using Anaconda, don't forget to activate your environment by `activate env_name`(you can find your environment name by `conda env list`). Or you might see the error  
```
Drawing salary histogram for consultant(predicted by glassdoor)
This application failed to start because it could not find or load the Qt platform plugin "windows"
in "".

Available platform plugins are: direct2d, minimal, offscreen, windows.

Reinstalling the application may fix this problem.
```

* run Point_v1.py

 
