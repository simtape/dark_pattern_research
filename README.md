# Dark Pattern Research

A tool used for an university project work to conduct a web investigation among the most popular italian websites with the scope to find possible usage of deceptive design in the cookie banners.

# Project organization
```
├── data
│   ├── csv_files
│   ├── results
│   └── screenshots
│       ├── detected_banners
│       └── visited_websites
└── utilities
    ├── search_handlers
    ├── __init.py
    ├── BannerDetector.py
    ├── ButtonElement.py
    ├── dark_pattern_heuristics.py
    ├── .gitignore
    └── README.md
    
```

## Requirements
Requirements can be installed by using the command
```
pip install -r requirements.txt
```

# Getting started
The tool has three main functionalities: 
    -   detection of a banner in a website;
    -   scraping of elements contained in a banner;
    -   performing an analysis on the collected data, in order to find possible violations.

To start the tool is enough executing the main.py by the command

```
python3 main.py
```
Before doing this, according to the analysis to perform, it's necessary to call the specific methods.
## Banner detection
To perform the detection of banners off a list of websites, call in main.py the method
```
startBannerDetection()
```
In the file ``` BannerDetector```, specify the name of the list (csv format) of websites to analyze.
## Banner scraping
Firstly, you have to set up the backend in order to store the collected elements from the banner.
Get the backend here -> https://github.com/simtape/dark-pattern-backend and follow the instruction in the READme to set it up.
To perform the scraping of elements off banners, call in main.py the method
```
startButtonDetection()
```
In the file ``` BannerDetector```, specify the name of the list (csv format) of websites to analyze.
## Analysis of data

To perform the detection of deceptive elements and so the production of results, call in main.py the method
```
start_analysis(<your_address_of_localhost_backend>)
```
Before starting the analysis, fire up the backend locally. 

