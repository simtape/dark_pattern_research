from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.color import Color

class ButtonElement:
    def __init__(self, btnElem: WebElement):
        self.text = None
        self.color = None
        self.textColor = None
        self.type = None
        self.redirect = None
        self.html = None
        self.size = None
        self.second_layer = False
        self.ambiguous_text = False
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

    def getDataButton(self):
        return {
            "text": self.text,
            "ambiguous_text": self.ambiguous_text,
            "second_layer": self.second_layer,
            "color": self.color,
            "text_color": self.textColor,
            "type": self.type,
            "redirect": self.redirect,
            "html": self.html,
            "size": self.size
        }



