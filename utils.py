import json
import os

from selenium.webdriver import Chrome as Driver
from selenium.webdriver.remote.webelement import WebElement

home_dir = os.path.expanduser("~")
file_path = os.path.join(home_dir, "sophos_credentials.json")


def save_credentials_file(data: dict[str, str]) -> None:
    with open(file_path, "w") as f:
        json.dump(data, f)
        print(f"Credentials saved successfully to {file_path}")


def load_credentials() -> dict[str, str] | str:
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return "FileNotFoundError"
    except json.decoder.JSONDecodeError:
        return "JSONDecodeError"
    except Exception as e:
        return f"Error: {e}"


def click_element(driver: Driver, element: WebElement) -> Driver:
    driver.execute_script("arguments[0].click();", element)
    return driver


# save_credentials_file({"username": "admin", "password": "admin"})
# print(load_credentials())
