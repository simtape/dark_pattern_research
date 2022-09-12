from selenium.webdriver.common.by import By

from utilities.search_handlers.DetectorHandlers import startButtonDetection
from utilities.search_handlers.DetectorHandlers import startBannerDetection
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utilities.dark_pattern_heuristics import DarkPatternFinder, start_analysis

# startBannerDetection(number_of_websites=659)
#startButtonDetection()

start_analysis("http://127.0.0.1:8000/")
