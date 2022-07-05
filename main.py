import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
import csv
from CookieBanner import CookieBanner, BannerElement

SLEEP_TIME_CMP_WAIT = 3


# def executeCmpFunction(it_list):
#     csvreader = csv.reader(it_list)
#     options = Options()
#     options.add_argument("--headless")
#     driver = webdriver.Chrome(options=options)
#     visitedwebsites = []
#
#     for website_name in csvreader:
#         url = "https://" + website_name
#         driver.get(url)
#         time.sleep(SLEEP_TIME_CMP_WAIT)
#
#         try:
#             driver.execute_script('if (__tcf) return "ok";', None)
#             print('__tcf found')
#             cookie_banner = CookieBanner(url, driver)
#             cookie_banner.spot_banner_buttons()
#             #website.tcfexists = True
#         except JavascriptException as e:
#             print('__tcf not found: ', e)
#
#     print(visitedwebsites)

def checkTCFandFindButtons(it_list):
    tcfwebsitefile = 'tcfwebsites.csv'
    csvreader = csv.reader(it_list)
    tcfwebsites = []

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        for row in csvreader:
            str = row[0]
            print(str)
            try:
                time.sleep(SLEEP_TIME_CMP_WAIT)
                driver.get("https://" + str)
            except WebDriverException as e:
                print(e.stacktrace)
            try:
                driver.execute_script('if (__tcfapi) return "ok";', None)
                print('__tcf found')
                tcfwebsites.append(str)
            except Exception as e:
                continue
            try:
                with open(tcfwebsitefile, 'w', newline='') as fl:
                    writer = csv.writer(fl)
                    for website in tcfwebsites:
                        writer.writerow([website])
            except BaseException as e:
                print('BaseException:', fl)
    # website.tcfexists = True
    except JavascriptException as e:
        print('__tcf not found: ', e)


# cookie_banner = CookieBanner(driver)
# cookie_banner.spot_banner_buttons()


# takes as input the tranco list with the top 1M websites
# and creates a csv with only italian domain web sites
def filterList(tranco_list):
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


# tranco_list = open('tranco_25JP9.csv')
# filterList(tranco_list)
it_list = open('itwebsites.csv')
checkTCFandFindButtons(it_list)
