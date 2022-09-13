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

        if "buttons" in self.banner and self.banner["buttons"] is not None:
            self.exist_buttons = True
        else:
            self.exist_buttons = False

    def exists_color_mismatch(self):

        if self.banner["buttons"]["approve_btn"] is not None and self.banner["buttons"]["deny_btn"] is not None:
            if self.banner["buttons"]["approve_btn"]["color"] is not None and self.banner["buttons"]["deny_btn"][
                "color"] is not None:
                if self.banner["buttons"]["approve_btn"]["color"] != self.banner["buttons"]["deny_btn"]["color"]:
                    self.color_mismatch = True
                else:
                    self.color_mismatch = False
        else:
            self.color_mismatch = False

    def exists_size_mismatch(self):
        if self.banner["buttons"]["approve_btn"] is not None and self.banner["buttons"]["deny_btn"] is not None:
            approve_btn_height = self.banner["buttons"]["approve_btn"]["size"]["height"]
            approve_btn_width = self.banner["buttons"]["approve_btn"]["size"]["width"]

            deny_btn_height = self.banner["buttons"]["deny_btn"]["size"]["height"]
            deny_btn_width = self.banner["buttons"]["deny_btn"]["size"]["width"]

            if approve_btn_height > deny_btn_height or approve_btn_width > deny_btn_width:
                self.size_mismatch = True
            else:
                self.size_mismatch = False
        else:
            self.size_mismatch = False

    def no_way_to_opt(self):
        if self.banner["buttons"]["deny_btn"] is not None:
            deny_btn = self.banner["buttons"]["deny_btn"]

            if deny_btn["second_layer"] is not None:
                self.no_way_opt_first_layer = deny_btn["second_layer"]
                self.no_way_opt_second_layer = False
            else:
                self.no_way_opt_first_layer = deny_btn["second_layer"]
                self.no_way_opt_second_layer = False
        else:
            self.no_way_opt_first_layer = True
            self.no_way_opt_second_layer = True

    def exists_redirect(self):
        if self.banner["buttons"]["deny_btn"] is not None:
            redirect = self.banner["buttons"]["deny_btn"]["redirect"]
            if redirect is not None:
                self.redirect = True
            else:
                self.redirect = False
        else:
            self.redirect = False

        return

    def no_way_to_manage_preferences(self):
        if self.banner["buttons"]["more_btn"] is not None:
            self.manage_preferences = True
        else:
            self.manage_preferences = False
            return

    def exists_cookie_policy(self):
        if self.banner["buttons"]["cookie_policy"] is not None:
            self.cookie_policy = True
        else:
            self.cookie_policy = False

    def ambiguous_text_finder(self):

        if self.banner["buttons"]["deny_btn"] is not None:
            deny_btn = self.banner["buttons"]["deny_btn"]

            if deny_btn["ambiguous_text"] is not None:
                self.ambiguous_text = deny_btn["ambiguous_text"]
        else:
            self.ambiguous_text = False
        return

    def generate_result(self):
        if (self.exist_buttons):
            self.ambiguous_text_finder()
            self.exists_color_mismatch()
            self.exists_redirect()
            self.exists_size_mismatch()
            self.no_way_to_opt()

            data = {
                "url": self.banner["url"],
                "color_mismatch": self.color_mismatch,
                "size_mismatch": self.size_mismatch,
                "no_way_to_opt_first_layer": self.no_way_opt_first_layer,
                "no_way_to_opt_second_layer": self.no_way_opt_second_layer,
                "redirect": self.redirect,
                "ambiguous_text": self.ambiguous_text,
                "dark_pattern_score": self.calculate_score()
            }

            return data
        else:
            data = {
                "url": self.banner.url,
                "info": "buttons not detected"
            }
            return data

    def calculate_score(self):
        score = 0
        if self.redirect and self.redirect is not None:
            score += 3

        if self.color_mismatch and self.color_mismatch is not None:
            score += 1

        if self.size_mismatch and self.size_mismatch is not None:
            score += 1

        if self.no_way_opt_first_layer and self.no_way_opt_first_layer is not None:
            score += 4

        if self.no_way_opt_second_layer and self.no_way_opt_first_layer is not None:
            score += 2

        if self.ambiguous_text and self.ambiguous_text is not None:
            score += 2

        return score


def start_analysis(api_url):
    response = requests.get(api_url)
    data = response.json()
    statistics = {}
    results = []
    print(data)
    for banner in data:
        if banner["url"] == "https://perugiatoday.it":
            break
        if banner["buttons"] is not None:
            if banner["buttons"]["deny_btn"] is not None and banner["buttons"]["approve_btn"] is not None and banner["buttons"]["more_btn"] is not None and banner["buttons"]["cookie_policy"] is not None:
                dark_pattern_finder = DarkPatternFinder(banner)
                results.append(dark_pattern_finder.generate_result())

    response2 = requests.get("http://127.0.0.1:8000/get_banners_sorted_second")
    data2 = response2.json()
    for banner in data2:
        if banner["buttons"] is not None:
            if banner["buttons"]["deny_btn"] is not None and banner["buttons"]["approve_btn"] is not None and \
                    banner["buttons"]["more_btn"] is not None and banner["buttons"]["cookie_policy"] is not None:
                dark_pattern_finder = DarkPatternFinder(banner)
                results.append(dark_pattern_finder.generate_result())

    sites_with_score_zero, sites_with_score_max, total_of_score = 0, 0, 0
    total_number_of_color_violation = 0
    total_number_of_size_violation = 0
    total_number_of_no_way_first_violation = 0
    total_number_of_no_way_second_violation = 0
    total_number_of_redirect_violation = 0
    total_number_of_ambiguous_violation = 0


    for result in results:
        total_of_score += result["dark_pattern_score"]
        if result["dark_pattern_score"] == 0:
            sites_with_score_zero += 1

        if result["dark_pattern_score"] == 13:
            sites_with_score_max += 1

        if result["color_mismatch"] == True:
            total_number_of_color_violation += 1

        if result["size_mismatch"] == True:
            total_number_of_size_violation += 1

        if result["no_way_to_opt_first_layer"] == True:
            total_number_of_no_way_first_violation += 1

        if result["no_way_to_opt_second_layer"] == True:
            total_number_of_no_way_second_violation += 1

        if result["redirect"] == True:
            total_number_of_redirect_violation += 1

        if result["ambiguous_text"] == True:
            total_number_of_ambiguous_violation += 1

    statistics = {"sites_with_score_zero": sites_with_score_zero,
                  "sites_with_score_max": sites_with_score_max,
                  "score_average": total_of_score/len(results),
                  "total_number_of_color_violation": total_number_of_color_violation,
                  "total_number_of_size_violation": total_number_of_size_violation,
                  "total_number_of_no_way_first_violation": total_number_of_no_way_first_violation,
                  "total_number_of_no_way_second_violation": total_number_of_no_way_second_violation,
                  "total_number_of_redirect_violation": total_number_of_redirect_violation,
                  "total_number_of_ambiguous_violation": total_number_of_ambiguous_violation
                  }
    statistics_file = open("data/results/statistics.json", "w")
    statistics_string = json.dumps(statistics)
    statistics_file.write(statistics_string)
    statistics_file.close()


    results_file = open("data/results/results_heuristics.json", "w")
    results_string = json.dumps(results)
    results_file.write(results_string)
    results_file.close()

