import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class TestBookingPlace:
    """Test class for booking a place"""

    def test_booking_places(self):
        """Login to the site, book a competition place and log out"""
        email = "john@simplylift.co"
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install())
        )

        driver.get("http://127.0.0.1:5000/")
        time.sleep(2)
        assert "GUDLFT Registration" in driver.title

        driver.find_element(By.TAG_NAME, "input").send_keys(email + Keys.ENTER)
        time.sleep(2)
        assert "Summary | GUDLFT Registration" in driver.title

        link = driver.find_element(By.LINK_TEXT, "Book Places")
        link.click()
        time.sleep(2)
        assert "Booking for" in driver.title

        driver.find_element(By.NAME, "places").send_keys("0" + Keys.ENTER)
        time.sleep(2)
        assert "Summary | GUDLFT Registration" in driver.title

        link = driver.find_element(By.LINK_TEXT, "Logout")
        link.click()
        time.sleep(2)
        assert "GUDLFT Registration" in driver.title

        time.sleep(2)
        driver.close()
