import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager
import csv
import cv2 as cv
import pytesseract

SLEEP_TIME_CMP_WAIT = 2


class BannerDetector:
    websites_with_banners = []

    def __init__(self, website_list, csv_path):
        self.website_list = website_list
        self.csv_path = csv_path

    def banners_research(self):
        options = Options()

        options.add_argument("--headless")
        # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        driver =webdriver.Chrome(ChromeDriverManager().install(), options = options)

        print(self.website_list)
        for website in self.website_list:
            print("sito: " + website)
            url = website
            try:
                driver.get("https://" + url)
                #time.sleep(SLEEP_TIME_CMP_WAIT)
                driver.save_screenshot("data/screenshots/visited_websites/" + website + ".png")
                self.__banner_detection(website + ".png", url)
            except BaseException as e:
                print('BaseException:', e)

        self.generate_csv()


    def __banner_detection(self, url_image, website_url):
        image = cv.imread("data/screenshots/visited_websites/" + url_image)
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        _, thrash = cv.threshold(gray_image, 240, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        for contour in contours:
            shape = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
            x_cor = shape.ravel()[0]
            y_cor = shape.ravel()[1]

            if len(shape) == 4:
                x, y, w, h = cv.boundingRect(shape)

                # aspectRatio = float(w) / h
                cv.drawContours(image, [shape], 0, (0, 255, 0), 4)
                cropped = image[y:y + h, x:x + w]
                text = pytesseract.image_to_string(cropped, lang="ita")

                if text and "cookie" in text:
                    cv.putText(image, "Banner", (x_cor, y_cor), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                    cv.imwrite('data/screenshots/detected_banners/detected_' + url_image, image)
                    self.websites_with_banners.append(website_url)

    def generate_csv(self):
        try:
            with open(self.csv_path, 'w', newline='') as fl:
                writer = csv.writer(fl)
                for website in self.websites_with_banners:
                    writer.writerow([website])

        except BaseException as e:
            print('BaseException:', fl)
