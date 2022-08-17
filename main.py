import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
import csv
from CookieBanner import CookieBanner, BannerElement
import cv2 as cv
import pytesseract
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

def checkTCFandFindButtons():
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


def detectBanner():

    image = cv.imread('fanpage_banner.png')

    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # find threshold of the image
    _, thrash = cv.threshold(gray_image, 240, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    for contour in contours:
        shape = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
        x_cor = shape.ravel()[0]
        y_cor = shape.ravel()[1]

        if len(shape) == 4:
            # shape cordinates
            x, y, w, h = cv.boundingRect(shape)

            # width:height
            aspectRatio = float(w) / h
            cv.drawContours(image, [shape], 0, (0, 255, 0), 4)
            cropped = image[y:y + h, x:x + w]
            text = pytesseract.image_to_string(cropped, lang="ita")

            if text and "cookie" in text:
                cv.putText(image, "Banner", (x_cor, y_cor), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

    cv.imshow("Shape", image)
    cv.waitKey(0)
    cv.destroyAllWindows()

# tranco_list = open('tranco_25JP9.csv')
# filterList(tranco_list)

#checkTCFandFindButtons()
# executeCmpFunction(itwebsites)
detectBanner()
