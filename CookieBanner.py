from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

class CookieBanner:

	def __init__(self, url, web_driver: webdriver):
		self.web_driver = web_driver
		self.url: url
		self.approve_btn = None
		self.reject_btn = None
		self.more_btn = None


	def spot_banner_buttons(self):
		approve_word_keys = [
			"accetto",
			"sono d'accordo",
			"accetta",
			"accetta tutto",
			"ok",
			"accetta tutti"
			"csdcever"
		]

		deny_word_keys = [
			# "rifiuta",
			# "non sono d'accordo"
			"freverv"
		]
		approve_btn = self.spot_a_btn(approve_word_keys)
		deny_btn = self.spot_a_btn(deny_word_keys)

		if approve_btn:
			approve_btn = BannerElement(approve_btn);
			approve_btn.screenshot()

		if deny_btn:
			print("Trovato rifiuta")


	def spot_a_btn(self, word_keys):

		# looking for a button, an input field or a link
		# since web sites banner not only use buttons
		# for accept/reject cookie
		elements_type = ["button", "input", "a"]
		for type in elements_type:
			elements = self.web_driver.find_elements(By.TAG_NAME, type)

			for element in elements:

				element_text = element.text or element.get_attribute("value")
				if not element_text:
					continue
				element_text = "".join(char for char in element_text if char.isalpha())
				element_text = "".join(element_text.lower().split())


				for word_key in word_keys:
					if word_key in element_text:
						return element


		return None


class BannerElement:
	def __init__(self, element: WebElement):
		self.element = element

	def screenshot(self):
		self.element.screenshot("data/screenshots/pic1.png")

