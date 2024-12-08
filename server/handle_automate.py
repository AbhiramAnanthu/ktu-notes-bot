from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import logging


class HandleAutomation:
    def __init__(self):
        self._initialize_driver()

    def _initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "prefs",
            {
                "safebrowsing.enabled": True,
            },
        )
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=chrome_options, service=s)

    def extract_urls(self, subject: dict) -> dict:
        url = self._create_url(subject)
        try:
            self.driver.get(url)
            logging.info(f"Accessed URL: {url}")
            download_elements = self.driver.find_elements(
                by=By.CLASS_NAME, value="elementor-button"
            )
            keys = [
                element.find_element(By.CLASS_NAME, "elementor-button-text").text
                for element in download_elements
            ]
            urls = [element.get_attribute("href") for element in download_elements]

            gdrive_links = dict(zip(keys, urls))
            # for link in gdrive_links.keys():
            #     gdrive_links[link] = self._download_link(gdrive_links[link])

            return gdrive_links
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            self.driver.close()

    def _create_url(self, subject: dict) -> str:
        if "code" not in subject or "name" not in subject:
            raise ValueError("Subject dictionary must contain 'code' and 'name' keys")
        sub_code = subject["code"]
        sub_name = subject["name"]

        url = f"https://www.ktunotes.in/ktu-{sub_code}-{sub_name}-notes/"
        return url

    def _download_link(self, link: str) -> str:
        pattern = r"/d/([a-zA-Z0-9_-]+)"
        match = re.search(pattern, link)
        if not match:
            raise ValueError(f"Invalid Google Drive link: {link}")
        id = match.group(1)
        url = f"https://drive.usercontent.google.com/u/0/uc?id={id}&export=download"
        return url
