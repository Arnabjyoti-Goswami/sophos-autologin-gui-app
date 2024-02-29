from time import sleep as s

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver import Edge as EdgeDriver
from selenium.webdriver import Firefox as FirefoxDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located as element_present,
)
from selenium.webdriver.support.ui import WebDriverWait as wait

from utils import click_element


class SophosLogin:
    def __init__(
        self,
        browser_name: str,
        binary_location: str = "",
        url: str = "http://172.16.0.30:8090/httpclient.html",
    ):
        self.browser_name = browser_name
        self.binary_location = binary_location
        self.url = url

    def _configure_options(
        self,
        options: ChromeOptions | EdgeOptions | FirefoxOptions,
    ) -> ChromeOptions | EdgeOptions | FirefoxOptions:
        options.binary_location = self.binary_location
        options.headless = True
        options.add_argument(
            "--log-level=3"
        )  # ignore INFO and WARNINGS, only display errors in the console
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-default-apps")
        return options

    def init_driver(self) -> ChromeDriver | EdgeDriver | FirefoxDriver | str:
        try:
            if self.browser_name == "chrome":
                chrome_options = ChromeOptions()
                chrome_options = self._configure_options(chrome_options)
                driver = ChromeDriver(options=chrome_options)
            elif self.browser_name == "firefox":
                firefox_options = FirefoxOptions()
                firefox_options = self._configure_options(firefox_options)
                driver = FirefoxDriver(options=firefox_options)
            elif self.browser_name == "edge":
                edge_options = EdgeOptions()
                edge_options = self._configure_options(edge_options)
                driver = EdgeDriver(options=edge_options)
            else:
                raise ValueError("Invalid choice")

            return driver

        except Exception as err:
            return f"An error occurred: {err}"

    def login(self, username: str, password: str) -> str:
        try:
            driver = self.init_driver()

            if isinstance(driver, str):
                return driver

            driver.get(self.url)
            username_input_xpath = f"/html/body/font/font/font/font/div/div[1]/div[2]/div[1]/div[1]/input[1]"
            username_input = wait(driver, 10).until(
                element_present((By.XPATH, username_input_xpath))
            )
            password_input_xpath = f"/html/body/font/font/font/font/div/div[1]/div[2]/div[1]/div[1]/input[2]"
            password_input = wait(driver, 10).until(
                element_present((By.XPATH, password_input_xpath))
            )

            username_input.send_keys(username)
            password_input.send_keys(password)

            login_button_xpath = (
                f"/html/body/font/font/font/font/div/div[1]/div[2]/div[3]/a/div"
            )
            login_button = driver.find_element("xpath", login_button_xpath)
            driver = click_element(driver, login_button)

            s(2)

            driver.quit()

            return "Login successful!"
        except TimeoutException as err:
            return f"An error occurred: The page took too long to load \n{err}"
        except Exception as err:
            return f"An error occurred: {err}"
