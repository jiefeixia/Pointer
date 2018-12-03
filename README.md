# Pointer
This is the Course project for Data Focus Python. You can use this program to find your desired job!


# Instruction
Welcome page "welcome to Pointer", Choose:  
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
        * Course Evaluation Score    
    * Show Recommended Job (enter optional preferred location):
        * Job Name
        * Company Name
        * Average Salary
        * Location
3. Update and clean
    * Crawl job data from glassdoor.com
        * ds.csv
        * sde.csv
        * consultant.csv
    * Crawl course evluation data from smartevl.com
        * course_evl.csv
    * Crawl course infomation data from heinz.cmu.edu.com
        * course_info.csv
    * Download data from pillow.com and convert it into desired file
        * rent_price.csv
    * Get data from arcgis API
        * company_loc.csv
        
        
        
# Installation
* Download the whole folder and decompression
* Required environment: python 3.5+
* Required packages: `requirement.txt`. You can install by `pip install -r requirement.txt`
* If you are using Anaconda, don't forget to activate your environment by `activate env_name`(you can find your environment name by `conda env list`). Or you might see the error  
```bash
Drawing salary histogram for consultant(predicted by glassdoor)
This application failed to start because it could not find or load the Qt platform plugin "windows"
in "".

Available platform plugins are: direct2d, minimal, offscreen, windows.

Reinstalling the application may fix this problem.
```

* run Point_v1.py

 
