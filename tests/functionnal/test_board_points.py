import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class TestBoardPoints:
    """Test class for navigation to board points url"""

    def test_navigate_to_board_points(self):
        """Access to the points table page"""
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install())
        )
        driver.get("http://127.0.0.1:5000/clubs_points")
        assert "Board Clubs points" in driver.title
        time.sleep(2)
        driver.close()
