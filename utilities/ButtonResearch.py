import sys
import os
from selenium import webdriver
from loguru import logger as log
import requests
from datetime import datetime
from utilities.ButtonElement import ButtonElement
from selenium.webdriver.common.by import By

mainPath = os.path.abspath(os.getcwd())
post_url = "http://127.0.0.1:8000/cookie_banner"

class Button:
    def __init__(
            self, url: str, web_driver: webdriver
    ):
        self.url = url
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
        approve_word_keys = [
            "accetto",
            "sonod'accordo",
            "accetta",
            "accettatutto",
            "ok",
            "accettatutti",
            "accettoilmonitoraggio",
            "accettaechiudi",
            "accettatuttiicookie"
        ]
        apprBtn = self.button_types(approve_word_keys)
        if apprBtn:
            log.debug("FOUND APPROVE BUTTON!")
            apprBtn = ButtonElement(apprBtn)
            self.apprBtn = apprBtn
            self.apprBtnMeta = apprBtn.getDataButton()
        policy_word_keys = [
            "privacypolicy",
            "cookiepolicy"
        ]
        policyBtn = self.button_types(policy_word_keys)
        if policyBtn:
            log.debug("FOUND COOKIE POLICY BUTTON!")
            policyBtn = ButtonElement(policyBtn)
            self.policyBtn = policyBtn
            self.policyBtnMeta = policyBtn.getDataButton()

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
            "preferenzedeicookie"
        ]
        moreBtn = self.button_types(preferences_word_keys)
        moreBtnclick = moreBtn
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
            "confermalemiescelte"
        ]
        denyBtn = self.button_types(deny_word_keys)
        denyBtnAmbiguous = self.button_types(deny_word_keys_ambiguous)
        if denyBtn:
            log.debug("FOUND REJECT BUTTON!")
            denyBtn = ButtonElement(denyBtn)
            self.denyBtn = denyBtn
            self.denyBtn.second_layer = False
            self.denyBtn.ambiguous_text =False
            self.denyBtnMeta = denyBtn.getDataButton()
        elif denyBtnAmbiguous:
            log.debug("FOUND REJECT BUTTON WITH AMBIGUOUS TEXT")
            denyBtnAmbiguous = ButtonElement(denyBtnAmbiguous)
            self.denyBtn = denyBtnAmbiguous
            self.denyBtn.second_layer = False
            self.denyBtn.ambiguous_text = True
            self.denyBtnAmbiguousMeta = denyBtnAmbiguous.getDataButton()
        elif moreBtn:
            moreBtnclick.click()
            denyBtnSecondLayer = self.button_types(deny_word_keys)
            denyBtnAmbiguousSecondLayer = self.button_types(deny_word_keys_ambiguous)
            if denyBtnSecondLayer:
                log.debug("FOUND REJECT BUTTON IN SECOND LAYER!")
                denyBtnSecondLayer = ButtonElement(denyBtnSecondLayer)
                self.denyBtn = denyBtnSecondLayer
                self.denyBtn.second_layer = True
                self.denyBtn.ambiguous_text = False
                self.denyBtnMeta = denyBtnSecondLayer.getDataButton()
            elif denyBtnAmbiguousSecondLayer:
                log.debug("FOUND REJECT BUTTON WITH AMBIGUOUS TEXT IN SECOND LAYER")
                denyBtnAmbiguousSecondLayer = ButtonElement(denyBtnAmbiguousSecondLayer)
                self.denyBtn = denyBtnAmbiguousSecondLayer
                self.denyBtn.second_layer = True
                self.denyBtn.ambiguous_text = True
                self.denyBtnAmbiguousMeta = denyBtnAmbiguousSecondLayer.getDataButton()




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

    def getData(self):
        return {
            "more_btn": self.moreBtnMeta,
            "deny_btn": self.denyBtnMeta,
            "approve_btn": self.apprBtnMeta,
            "cookie_policy": self.policyBtnMeta,
        }

    @log.catch
    def doResearch(self):
        try:
            self.startedAt = datetime.now()
            self.web_driver.delete_all_cookies()
            self.web_driver.get(self.url)
            self.find_buttons()
            buttons = self.getData()

            if buttons:
                self.endedAt = datetime.now()
                data = {
                    "website_url": self.url,
                    "status": "runDone",
                    "buttons": buttons,
                }
                response = requests.post(post_url, json=data)
                print(response.json())
            else:
                self.endedAt = datetime.now()
                data = {
                    "website_url": self.url,
                    "status": "noDataFound",
                    "buttons": None

                }
                response = requests.post(post_url, json=data)
                print(response.json())
            log.info("DONE!")
        except:
            e = sys.exc_info()[0]
            log.exception(e)