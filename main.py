
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

