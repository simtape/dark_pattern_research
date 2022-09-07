import sys
import os
import splinter
import selenium
from loguru import logger as log
from splinter import Browser as Sbrowser
from selenium import webdriver as wd
from selenium.webdriver.support.color import Color
from datetime import datetime
from utilities.ButtonDetection import find_cookie_banner
import requests

mainPath = os.path.abspath(os.getcwd())
post_url = "http://127.0.0.1:8000/cookie_banner"

class Button:
    def __init__(
            self, url, consent_elem: selenium.webdriver.remote.webelement.WebElement
    ):
        self.url = url
        self.elem = consent_elem
        self.size = self.elem.size
        self.links = []
        self.text = self.elem.text
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
        self.html = self.elem.get_attribute("outerHTML")
        for elem in self.elem.find_elements_by_partial_link_text(""):
            self.links.append(elem.get_attribute("href"))
        self.find_buttons()

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
        ]
        moreBtn = self.spot_a_btn(preferences_word_keys)
        if moreBtn:
            log.debug("FOUND MORE BUTTON!")
            moreBtn = ButtonElement(moreBtn)
            self.moreBtn = moreBtn
            self.moreBtnMeta = moreBtn.getMeta()

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
        ]
        denyBtn = self.spot_a_btn(deny_word_keys)
        denyBtnAmbiguous = self.spot_a_btn(deny_word_keys_ambiguous)
        if denyBtn:
            log.debug("FOUND REJECT BUTTON!")
            denyBtn = ButtonElement(denyBtn)
            self.denyBtn = denyBtn
            self.denyBtnMeta = denyBtn.getMeta()
        else:
            log.debug("FOUND REJECT BUTTON WITH AMBIGUOUS TEXT")
            denyBtnAmbiguous = ButtonElement(denyBtnAmbiguous)
            self.denyBtnAmbiguous = denyBtnAmbiguous
            self.denyBtnAmbiguousMeta = denyBtnAmbiguous.getMetaAmbiguous()

        approve_word_keys = [
            "accetto",
            "sonod'accordo",
            "accetta",
            "accettatutto",
            "ok",
            "accettatutti",
            "accettoilmonitoraggio",
            "accettaechiudi",
        ]
        apprBtn = self.spot_a_btn(approve_word_keys)
        if apprBtn:
            log.debug("FOUND APPROVE BUTTON!")
            apprBtn = ButtonElement(apprBtn)
            self.apprBtn = apprBtn
            self.apprBtnMeta = apprBtn.getMeta()
        policy_word_keys = [
            "privacy policy",
        ]
        policyBtn = self.spot_a_btn(policy_word_keys)
        if policyBtn:
            log.debug("FOUND POLICY BUTTON!")
            policyBtn = ButtonElement(policyBtn)
            self.policyBtn = policyBtn
            self.policyBtnMeta = policyBtn.getMeta()
        else:
            policyBtn = self.spot_policy_link()
            policyBtn = ButtonElement(policyBtn)
            self.policyBtn = policyBtn
            self.policyBtnMeta = policyBtn.getMeta()

    @log.catch
    def spot_a_btn(self, triggers):
        elemTypes = ["button", "input", "a"]
        for t in elemTypes:
            elems = self.elem.find_elements_by_tag_name(t)
            for elem in elems:
                elemText = elem.text or elem.get_attribute("value")
                if not elemText:
                    continue
                elemText = "".join(char for char in elemText if char.isalpha())
                elemText = "".join(elemText.lower().split())
                for trig in triggers:
                    if trig == elemText:
                        return elem
        return None

    @log.catch
    def spot_policy_link(self):
        xpaths = ["//a[contains(@href,'cookie')]", "//a[contains(@href,'policy')]"]
        for xpath in xpaths:
            elem = self.elem.find_element_by_xpath(xpath)
            if elem:
                log.debug("FOUND COOKIE POLICY LINK ELEMENT.")
                return elem
        log.debug("Did not find any cookie policy link.")
        return None  # None found

    def getMeta(self):
        return {
            #"banner_size": self.size,
            "more_btn": self.moreBtnMeta,
            "deny_btn": self.denyBtnMeta,
            "approve_btn": self.apprBtnMeta,
            "cookie_policy": self.policyBtnMeta,
        }


class ButtonElement:

    def __init__(self, btnElem: selenium.webdriver.remote.webelement.WebElement):
        self.text = None
        self.color = None
        self.textColor = None
        self.type = None
        self.redirect = None
        self.html = None
        self.size = None
        if btnElem:
            self.elem = btnElem
            if self.elem:
                self.text = self.elem.text or self.elem.get_attribute("value")
                self.type = self.elem.tag_name
                self.html = self.elem.get_attribute("outerHTML")
            if self.elem.size:
                self.size = self.elem.size
            if self.elem.get_attribute("href"):
                self.redirect = self.elem.get_attribute("href")
            if self.elem.value_of_css_property("background-color"):
                self.color = Color.from_string(
                    self.elem.value_of_css_property("background-color")
                ).hex
            if self.elem.value_of_css_property("color"):
                self.textColor = Color.from_string(
                    self.elem.value_of_css_property("color")
                ).hex

    def getMeta(self):
        return {
            "text": self.text,
            "ambiguous_text": False,
            "color": self.color,
            "text_color": self.textColor,
            "type": self.type,
            "redirect": self.redirect,
            "html": self.html,
            "size": self.size,
        }

    def getMetaAmbiguous(self):
        return {
            "text": self.text,
            "ambiguous_text": True,
            "color": self.color,
            "text_color": self.textColor,
            "type": self.type,
            "redirect": self.redirect,
            "html": self.html,
            "size": self.size,
        }


@log.catch
class PageScanner:
    def __init__(
            self, browser: splinter.driver.DriverAPI,  url: str
    ):
        self.browser = browser
        self.windowSize = self.browser.driver.get_window_size()
        self.url = url
        self.consent = None

    def doScan(self):
        try:
            self.startedAt = datetime.now()
            self.browser.cookies.delete()
            self.browser.visit(self.url)

            consent = find_cookie_banner(self.browser)
            if consent:
                self.consent = Button(self.url, consent)
                self.endedAt = datetime.now()
                data = {
                        "status": "runDone",
                        "browser_size": str(self.windowSize),
                        "buttons": self.consent.getMeta(),
                    }
                print(data)
                print("ciao")
                response = requests.post(post_url, json=data)
                print(response.json())

            else:
                self.endedAt = datetime.now()
                data = {
                    "status": "noNoticeFound",
                    "browser_size": str(self.windowSize),
                    "buttons": None

                }
                response = requests.post(post_url, json=data)
                print(response.json())
                return None

            log.info("DONE!")
        except:
            e = sys.exc_info()[0]
            log.exception(e)


def setupDriver(hless=False):
    browserOptions = wd.ChromeOptions()
    browserOptions.add_argument("--window-size=1920,1080")
    browserOptions.add_experimental_option("w3c", True)
    browserOptions.headless = hless
    return Sbrowser("chrome", options=browserOptions)