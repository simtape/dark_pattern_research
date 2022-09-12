from utilities.search_handlers.DetectorHandlers import startButtonDetection, filter_csv
from utilities.dark_pattern_heuristics import DarkPatternFinder, start_analysis

# startBannerDetection(number_of_websites=659)
#startButtonDetection()

start_analysis("http://127.0.0.1:8000/get_banners_sorted")
