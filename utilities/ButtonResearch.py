import sys
import os
from selenium import webdriver
from loguru import logger as log
from selenium.webdriver.common.by import By
from pymongo import MongoClient, ReturnDocument
from datetime import datetime
from utilities.ButtonElement import ButtonElement

mainPath = os.path.abspath(os.getcwd())


class Database:

    def __init__(self, db_url=None):
        try:
            self.client = MongoClient(db_url)
            self.db = self.client["CookieBanner"]
            self.runs = self.db["runs"]
            status = self.status()
            log.debug(
                "Running MongoDB {} on host {}.",
                status["version"],
                status["host"],
                status["uptime"],
            )
        except Exception as e:
            log.exception(e)

    def status(self):
        try:
            status = self.db.command("serverStatus")
            return status
        except Exception as e:
            log.exception(e)

    def create_run(self, url):
        try:
            new_run = {
                "url": url,
                "status": "startingRun",
            }
            obj_id = self.runs.insert_one(new_run).inserted_id
            return obj_id
        except Exception as e:
            log.exception(e)

    def modify_run(self, run_id, data):
        try:
            run = self.runs.find_one_and_update(
                {"_id": run_id}, {"$set": data}, return_document=ReturnDocument.AFTER
            )
            return run
        except Exception as e:
            log.exception(e)

    def get_run(self, run_id):
        try:
            run = self.runs.find_one({"_id": run_id})
            return run
        except Exception as e:
            log.exception(e)


class Button:
    def __init__(
            self, url: str, web_driver: webdriver, db: Database
    ):
        self.url = url
        self.db = db
        self.web_driver = web_driver
        self.links = []
        self.apprBtn = None
        self.apprBtnMeta = None
        self.denyBtn = None
        self.denyBtnMeta = None
        self.denyBtnAmbiguous = None
        self.denyBtnAmbiguousMeta = None
        self.moreBtn = None
        self.moreBtnMeta = None
        self.policyBtn = None
        self.policyBtnMeta = None

    def find_buttons(self):
        preferences_word_keys = [
            "gestiscipreferenze",
            "gestisciopzioni",
            "impostazionedeicookie",
            "personalizzaleopzioni",
            "gestiscilemieimpostazioni",
            "gestisciimpostazioni",
            "piùopzioni",
            "gestionedelmonitoraggio",
            "impostazionicookie",
            "personalizza",
            "preferenzedeicookie",
        ]
        moreBtn = self.button_types(preferences_word_keys)
        if moreBtn:
            log.debug("FOUND MORE BUTTON!")
            moreBtn = ButtonElement(moreBtn)
            self.moreBtn = moreBtn
            self.moreBtnMeta = moreBtn.getDataButton()

        deny_word_keys = [
            "rifiuta",
            "rifiutatutto",
            "rifiuto",
            "rifiutatutti",
            "nonsonod'accordo",
            "continuasenzaaccettare",
            "rifiutanonessenziali",
            "nonaccettareechiudi",
            "nonaccettare"
        ]
        deny_word_keys_ambiguous = [
            "salvaedesci",
            "salvalemiescelte",
            "salva",
        ]
        denyBtn = self.button_types(deny_word_keys)
        denyBtnAmbiguous = self.button_types(deny_word_keys_ambiguous)
        if denyBtn:
            log.debug("FOUND REJECT BUTTON!")
            denyBtn = ButtonElement(denyBtn)
            self.denyBtn = denyBtn
            self.denyBtnMeta = denyBtn.getDataButton()
        elif denyBtnAmbiguous:
            log.debug("FOUND REJECT BUTTON WITH AMBIGUOUS TEXT")
            denyBtnAmbiguous = ButtonElement(denyBtnAmbiguous)
            self.denyBtnAmbiguous = denyBtnAmbiguous
            self.denyBtnAmbiguousMeta = denyBtnAmbiguous.getDataAmbiguous()
        elif moreBtn:
            log.debug("click")
            # cookie_button = self.elem.find_element_by_xpath("//button[text()='Preferenze dei cookie']")
            # cookie_button.click()

        approve_word_keys = [
            "accetto",
            "sonod'accordo",
            "accetta",
            "accettatutto",
            "ok",
            "accettatutti",
            "accettoilmonitoraggio",
            "accettaechiudi",
            "accettatuttiicookie",
        ]
        apprBtn = self.button_types(approve_word_keys)
        if apprBtn:
            log.debug("FOUND APPROVE BUTTON!")
            apprBtn = ButtonElement(apprBtn)
            self.apprBtn = apprBtn
            self.apprBtnMeta = apprBtn.getDataButton()
        policy_word_keys = [
            "privacy policy",
        ]
        policyBtn = self.button_types(policy_word_keys)
        if policyBtn:
            log.debug("FOUND COOKIE POLICY BUTTON!")
            policyBtn = ButtonElement(policyBtn)
            self.policyBtn = policyBtn
            self.policyBtnMeta = policyBtn.getDataButton()
        else:
            policyBtn = self.policy_link()
            policyBtn = ButtonElement(policyBtn)
            self.policyBtn = policyBtn
            self.policyBtnMeta = policyBtn.getDataButton()

    @log.catch
    def button_types(self, word_keys):
        elemTypes = ["button", "input", "a"]
        for type in elemTypes:
            elems = self.web_driver.find_elements(By.TAG_NAME, type)
            for elem in elems:
                elemText = elem.text or elem.get_attribute("value")
                if not elemText:
                    continue
                elemText = "".join(char for char in elemText if char.isalpha())
                elemText = "".join(elemText.lower().split())
                for word_key in word_keys:
                    if word_key == elemText:
                        return elem
        return None

    @log.catch
    def policy_link(self):
        xpaths = ["//a[contains(@href,'cookie')]", "//a[contains(@href,'policy')]"]
        for xpath in xpaths:
            elem = self.web_driver.find_element_by_xpath(xpath)
            if elem:
                log.debug("FOUND COOKIE POLICY LINK ELEMENT!.")
                return elem
        return None

    def getData(self):
        return {
            "moreBtn": self.moreBtnMeta,
            "denyBtn": self.denyBtnMeta,
            "approveBtn": self.apprBtnMeta,
            "cookiePolicy": self.policyBtnMeta,
        }

    @log.catch
    def doResearch(self):
        try:
            self.startedAt = datetime.now()
            self.runId = self.db.create_run(self.url)
            self.web_driver.delete_all_cookies()
            self.web_driver.get(self.url)
            self.find_buttons()
            cookies = self.getData()
            if cookies:
                self.endedAt = datetime.now()
                self.db.modify_run(
                    self.runId,
                    {
                        "status": "runDone",
                        "button": cookies
                    }
                )
            else:
                self.endedAt = datetime.now()
                self.db.modify_run(
                    self.runId,
                    {
                        "status": "noDataFound",
                    },
                )
                return None
            log.info("DONE!")
        except:
            e = sys.exc_info()[0]
            log.exception(e)




