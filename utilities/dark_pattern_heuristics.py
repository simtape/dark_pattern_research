import requests
import json


class DarkPatternFinder:

    def __init__(self, banner_to_analyze):
        self.banner = banner_to_analyze
        self.color_mismatch = None
        self.size_mismatch = None
        self.no_way_opt_first_layer = None
        self.no_way_opt_second_layer = None
        self.redirect = None
        self.manage_preferences = None
        self.cookie_policy = None
        self.ambiguous_text = None

    def exists_color_mismatch(self):
        if self.banner.buttons.more_btn and self.banner.buttons.more_btn:
            if self.banner.buttons.more_btn.color != self.banner.buttons.deny_btn.color:
                self.color_mismatch = True
            else:
                self.color_mismatch = False

    def exists_size_mismatch(self):
        more_btn_height = self.banner.buttons.more_btn.size.height
        more_btn_width = self.banner.buttons.more_btn.size.width

        deny_btn_height = self.banner.buttons.deny_btn.size.height
        deny_btn_width = self.banner.buttons.deny_btn.size.width

        if more_btn_height > deny_btn_height or more_btn_width > deny_btn_width:
            self.size_mismatch = True
        else:
            self.size_mismatch = False

    def no_way_to_opt_first_layer(self):
        return

    def no_way_to_opt_second_layer(self):
        return

    def exists_redirect(self):
        return

    def no_way_to_manage_preferences(self):
        return

    def exists_cookie_policy(self):
        return

    def ambiguous_text(self):
        return

    def generate_result(self):
        data = {
            "url": self.banner.url,
            "color_mismatch": self.color_mismatch,
            "size_mismatch": self.size_mismatch,
            "no_way_to_opt_first_layer": self.no_way_opt_first_layer,
            "no_way_to_opt_second_layer": self.no_way_opt_second_layer,
            "redirect": self.redirect,
            "manage_preferences": self.manage_preferences,
            "cookie_policy": self.cookie_policy,
            "ambiguous_text": self.ambiguous_text

        }

        return data



def start_analysis(api_url):
    response = requests.get(api_url)