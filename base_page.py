from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.driver.maximize_window()
        self.base_url = "https://www.i.ua/"
        self.load_page(self.base_url)

    def find_element_by_xpath(self, xpath, time=10):
        WebDriverWait(self.driver, time).until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
        return self.driver.find_element_by_xpath(xpath)

    def find_elements_by_xpath(self, xpath, time=10):
        WebDriverWait(self.driver, time).until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
        return self.driver.find_elements_by_xpath(xpath)

    def element_send_keys(self, xpath, keys):
        element = self.find_element_by_xpath(xpath)
        element.send_keys(keys)

    def element_click(self, xpath):
        self.find_element_by_xpath(xpath).click()

    def load_page(self, url):
        self.driver.get(url)

    def accept_alert(self):
        alert = WebDriverWait(self.driver, 15).until(expected_conditions.alert_is_present())
        alert.accept()

    def close(self):
        self.driver.quit()

    def implicitly_wait(self, time):
        self.driver.implicitly_wait(time)
