import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests


def test_reachability():
    for i in range(3):
        time.sleep(2)
        assert requests.get("http://127.0.0.1:5000/").status_code == 200
