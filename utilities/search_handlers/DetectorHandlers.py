import pandas as pd
import pandas
from selenium import webdriver
from utilities import BannerDetector as bd
from utilities.ButtonResearch import Button
from selenium.webdriver.chrome.options import Options

"""
wrapper functions of methods for detection
"""


# start detection and collection of buttons in a banner
def startButtonDetection():

    website_list_df = pandas.read_csv("data/csv_files/banner_detected_websites2.csv")
    website_list = website_list_df['website'].tolist()

    for url in website_list:
        url = "https://" + url
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        res = Button(url, driver)
        res.doResearch()



# remove duplicates from a csv
def filter_csv():
    data = pd.read_csv('data/csv_files/banner_detected_websites.csv')
    data.sort_values("website", inplace=True)
    data.drop_duplicates(subset=None, inplace=True)
    data.to_csv('data/csv_files/banner_detected_websites.csv', index=False)


# starts the detection of banners, with a given list of websites in input
def startBannerDetection(number_of_websites):
    website_list_df = pandas.read_csv("data/csv_files/itwebsites.csv", nrows=number_of_websites)
    csv_path = "data/csv_files/banner_detected_websites.csv"
    website_list = website_list_df['website'].tolist()

    banner_detector = bd.BannerDetector(website_list=website_list, csv_path=csv_path)
    banner_detector.banners_research()
