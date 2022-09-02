# This file contains multiple different detection algorithms

import splinter
from loguru import logger as log

def find_by_cookie_string(browser: splinter.driver.DriverAPI):
    found_elems = []
    elems = browser.find_by_xpath(
        "//body//*/text()[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cookie')]/parent::*"
    )
    for elem in elems:
        if (
            elem._element.tag_name != "script"
            and elem._element.tag_name != "style"
            and elem.visible
        ):
            found_elems.append(elem)
    return found_elems


def find_by_parent(browser, elems):
    found = []
    for elem in elems:
        f_elem = find_by_helper(browser, elem)
        if f_elem and f_elem._element.is_displayed():
            found.append(f_elem)
    if len(found) > 0:
        return found[0]._element
    return None


def get_parent(browser, elem):
    parent = elem.find_by_xpath("./..").first
    if parent:
        return parent
    return None


def find_by_helper(browser, elem):
    s_elem = elem
    while s_elem and get_parent(browser, s_elem).tag_name != "html":
        if s_elem._element.value_of_css_property("position") == "fixed":
            return s_elem
        s_elem = get_parent(browser, s_elem)
    return None


def find_cookie_banner(browser):
    base_elems = find_by_cookie_string(browser)
    elem = find_by_parent(browser, base_elems)
    if elem:
        return elem
    if elem:
        return elem
    if elem:
        return elem
    log.debug("Could not find any banner.")
    return None
