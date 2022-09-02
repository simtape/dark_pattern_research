import pandas as pd
import pandas
from utilities import BannerDetector as bd
from loguru import logger as log
from itertools import islice
import csv
from utilities.CookieBanner import Database, PageScanner, setupDriver


# start detection and collection of buttons in a banner
def startButtonDetection():
    runId = 0
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


# remove duplicates from a csv
def filter_csv():
    data = pd.read_csv('data/csv_files/already_banner_detected.csv')
    data.sort_values("website", inplace=True)
    data.drop_duplicates(subset=None, inplace=True)
    data.to_csv('data/csv_files/already_banner_detected.csv', index=False)


# starts the detection of banners, with a given list of websites in input
def bannerDetection():
    website_list_df = pandas.read_csv("data/csv_files/itwebsites.csv", nrows=878)
    csv_path = "data/csv_files/banner_detected_websites.csv"
    website_list = website_list_df['website'].tolist()

    banner_detector = bd.BannerDetector(website_list=website_list, csv_path=csv_path)
    banner_detector.banners_research()
