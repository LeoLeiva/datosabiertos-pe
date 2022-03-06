import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

# browser = webdriver.Chrome('./chromedriver_75')
# browser.get('http://www.google.com')
# assert 'Google' in browser.title
# elem = browser.find_element_by_name('p')  # Find the search box
# elem.send_keys('seleniumhq' + Keys.RETURN)
# browser.quit()


class TestsLinkOk(unittest.TestCase):

    def setUp(self):
        ChromeOptions = webdriver.ChromeOptions()
        ChromeOptions.add_argument("--headless")
        self.driver = webdriver.Chrome(
            '/usr/lib/chromium-browser/chromedriver', options=ChromeOptions)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def test_dataset(self):
        self.driver.get("https://www.datosabiertos.gob.pe/")
        dataset = self.driver.find_element_by_id("facetapi-link--199")
        dataset.click()
        self.assertTrue(
            'https://www.datosabiertos.gob.pe/search/type/dataset?sort_by=changed' == self.driver.current_url)

    def test_economy_and_finances(self):
        self.driver.get(
            "https://www.datosabiertos.gob.pe/search/type/dataset?sort_by=changed")
        economy = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div/div/section/div/div/div/div/div[1]/div/div[2]/div/div/ul/li[1]/a")
        economy.click()
        self.assertTrue(
            'https://www.datosabiertos.gob.pe/search/field_topic/econom%C3%ADa-y-finanzas-29/type/dataset?sort_by=changed' == self.driver.current_url)

    def test_format_csv(self):
        self.driver.get("https://www.datosabiertos.gob.pe/search/field_topic/econom%C3%ADa-y-finanzas-29/type/dataset?sort_by=changed")
        self.driver.find_element_by_xpath(
            "//*[@id='main']/div/section/div/div/div/div/div[1]/div/div[4]").click()
        time.sleep(4)
        self.driver.find_element_by_id("facetapi-link--9").click()
        time.sleep(1)
        self.assertTrue('csv-14' in self.driver.current_url)

    def test_search_donation(self):
        self.driver.get("https://www.datosabiertos.gob.pe/search/field_resources%253Afield_format/csv-14/field_topic/economía-y-finanzas-29/type/dataset?sort_by=changed")
        self.donaciones = self.driver.find_element_by_name("query")
        self.donaciones.send_keys("donaciones")
        self.driver.find_element_by_id("edit-submit-dkan-datasets").click()
        self.assertTrue ('1 Distribución de Datos' in self.driver.page_source)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
