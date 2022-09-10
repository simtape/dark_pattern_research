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
        approve_btn_height = self.banner.buttons.approve_btn.size.height
        approve_btn_width = self.banner.buttons.approve_btn.size.width

        deny_btn_height = self.banner.buttons.deny_btn.size.height
        deny_btn_width = self.banner.buttons.deny_btn.size.width

        if approve_btn_height > deny_btn_height or approve_btn_width > deny_btn_width:
            self.size_mismatch = True
        else:
            self.size_mismatch = False

    def no_way_to_opt(self):
        deny_btn = self.banner.buttons.deny_btn

        if not deny_btn:
            self.no_way_opt_first_layer: True
            self.no_way_opt_second_layer: True
        elif deny_btn.second_layer:
            self.no_way_opt_first_layer: True
            self.no_way_opt_second_layer: False
        else:
            self.no_way_opt_first_layer: False
            self.no_way_opt_second_layer: deny_btn.second_layer



    def exists_redirect(self):
        redirect = self.banner.buttons.deny_btn.redirect
        if redirect:
            self.redirect = True
        else:
            self.redirect = False
        return

    def no_way_to_manage_preferences(self):
        more_btn = self.banner.buttons.more_btn
        if not more_btn:
            self.manage_preferences: False
        else:
            self.manage_preferences: True
        return

    def exists_cookie_policy(self):
        cookie_policy = self.banner.buttons.cookie_policy
        if not cookie_policy:
            self.cookie_policy = False
        else:
            return True
        return

    def ambiguous_text(self):
        deny_btn = self.banner.buttons.deny_btn

        if deny_btn.ambiguous_text:
            self.ambiguous_text = True
        else:
            self.ambiguous_text = False

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