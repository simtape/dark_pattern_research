import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import *
import csv
from CookieBanner import CookieBanner
import pandas
from utilities import BannerDetector as bd

SLEEP_TIME_CMP_WAIT = 2


def check_tcf_and_find_btns():
    options = Options()

    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    # visitedwebsites = []

    url = "https://" + "repubblica.it"
    driver.get(url)
    time.sleep(SLEEP_TIME_CMP_WAIT)

    try:
        driver.execute_script('if (__tcfapi) return "ok";', None)
        print('__tcf found')
        cookie_banner = CookieBanner(url, driver)
        cookie_banner.spot_banner_buttons()
    # website.tcfexists = True
    except JavascriptException as e:
        print('__tcf not found: ', e)


# takes as input the tranco list with the top 1M websites
# and creates a csv with only italian domain web sites
def filter_list(tranco_list):
    itwebsitefile = 'itwebsites.csv'
    csvreader = csv.reader(tranco_list)
    italianwebsites = []

    try:
        for row in csvreader:
            str = row[1]
            if str.endswith('.it'):
                italianwebsites.append(str)

        try:
            with open(itwebsitefile, 'w', newline='') as fl:
                writer = csv.writer(fl)
                for website in italianwebsites:
                    writer.writerow([website])

        except BaseException as e:
            print('BaseException:', fl)

    except BaseException as e:
        print('BaseException:', tranco_list)


def filter_csv():
    data = pd.read_csv('data/csv_files/already_banner_detected.csv')
    data.sort_values("website", inplace=True)
    data.drop_duplicates(subset=None, inplace=True)
    data.to_csv('data/csv_files/already_banner_detected.csv', index=False)


# website_list_df = pandas.read_csv("data/csv_files/itwebsites.csv", nrows=500)
# csv_path = "data/csv_files/banner_detected_websites.csv"
# website_list = website_list_df['website'].tolist()
#
# banner_detector = bd.BannerDetector(website_list=website_list, csv_path=csv_path)
# banner_detector.banners_research()

filter_csv()
