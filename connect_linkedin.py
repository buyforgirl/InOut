# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import sys
import settings

class ConnectLinkedin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.linkedin.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.username = settings.username
        self.pwd = settings.pwd


    def test_connect_linkedin(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("login-email").clear()
        driver.find_element_by_id("login-email").send_keys(self.username)
        driver.find_element_by_id("login-password").clear()
        driver.find_element_by_id("login-password").send_keys(self.pwd)
        driver.find_element_by_name("submit").click()
        driver.find_element_by_css_selector("li[data-li-activity-type='addconnections'] > :first-child").click()
        driver.find_element_by_id("main-search-box").send_keys('people with recruiters title')
        driver.find_element_by_css_selector("button.search-button").click()
        connectButtons = driver.find_elements_by_link_text('Connect')
        for connectButton in driver.find_elements_by_link_text('Connect'):
            driver.execute_script("arguments[0].scrollIntoView(true);", connectButton)
            connectButton.click()
        driver.find_element_by_link_text("Sign Out").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
