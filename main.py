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
from loguru import logger as log
from itertools import islice
import csv
from CookieBanner import Database, PageScanner, setupDriver

runId = 0
if __name__ == "__main__":
    db = Database()
    url_list = []
    with open("url_list_2.csv", "r") as link_csv_file:
        csv_reader = csv.DictReader(link_csv_file)

        header = next(csv_reader)
        if header != None:
            for link in islice(csv_reader, 5000):
                http_string = "https://" + link["Domain"]
                url_list.append(http_string)

    for url in url_list:
        runId += 1
        browser = setupDriver(True)
        with log.contextualize(url=url):
            res = PageScanner(browser, db, url)
            res.doScan()
            browser.quit()

SLEEP_TIME_CMP_WAIT = 2


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


website_list_df = pandas.read_csv("data/csv_files/itwebsites.csv", nrows=878)
csv_path = "data/csv_files/banner_detected_websites.csv"
website_list = website_list_df['website'].tolist()

banner_detector = bd.BannerDetector(website_list=website_list, csv_path=csv_path)
banner_detector.banners_research()

# filter_csv()
