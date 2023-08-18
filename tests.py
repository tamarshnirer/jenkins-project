import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import requests


@pytest.fixture(scope='session')
def browser():
    # Set Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    # Create a WebDriver instance!
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(version='114.0.5735.90').install()),options=chrome_options)

    # Yield the driver instance!
    yield driver

    # Teardown - quit the driver after the tests
    driver.quit()


def test_reachability():
    for i in range(3):
        time.sleep(2)
        assert (requests.get("http://127.0.0.1:5000/").status_code == 200)


def test_locations(browser):
    driver = browser
    driver.get("http://127.0.0.1:5000/")
    locations = {"berlin": "Berlin", "tokyo": "Tokyo", "tel aviv": "Tel Aviv"}
    for i in locations.items():
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="city"]').send_keys(i[0])
        driver.find_element(By.XPATH, "/html/body/div/form/button").click()
        elements = driver.find_elements(By.XPATH, "//*[text()]")
        for element in elements:
            flag = 0
            text = element.text
            if i[1] in text:
                flag = 1
                break
        if flag == 0:
            raise ValueError
        driver.find_element(By.XPATH, "/html/body/div/button").click()


def test_location_not_found(browser):
    locations = ["asdsedrtf", "adsferdhtr", "SDftg"]
    for i in locations:
        driver = browser
        driver.get("http://127.0.0.1:5000/")
        driver.find_element(By.XPATH, '//*[@id="city"]').send_keys(i)
        driver.find_element(By.XPATH, "/html/body/div/form/button").click()
        time.sleep(2)
        elements = driver.find_elements(By.XPATH, "//*[text()]")
        for element in elements:
            flag = 0
            text = element.text
            if "not found" in text:
                flag = 1
                break
        if flag == 0:
            raise ValueError
