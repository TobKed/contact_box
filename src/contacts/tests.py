from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager


class BasePage(object):
    url = None

    def __init__(self, driver):
        self.driver = driver

    def fill_form(self, elem, value):
        elem.send_keys(value)

    def fill_form_by_id(self, form_element_id, value):
        elem = self.driver.find_element_by_id(form_element_id)
        return self.fill_form(elem, value)

    def navigate(self):
        self.driver.get(self.url)


class Homepage(BasePage):
    url = "http://localhost:8000"

    def getLoginform(self):
        return LogInPage(self.driver)


class LogInPage(BasePage):
    url = "http://127.0.0.1:8000/login/"

    def setUsername(self, username):
        self.fill_form_by_id("id_username", username)

    def setPassword(self, password):
        self.fill_form_by_id("id_password", password)

    def submit(self):
        self.driver.find_element_by_css_selector(".btn").click()
        # self.driver.find_element_by_xpath("//*[contains(text(), 'Login')]").click()


class WevDriverShowcase(StaticLiveServerTestCase):
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def test_google_test(self):
        self.browser.get("https://www.google.com/")
        elem = self.browser.find_element_by_name("q")
        sleep(1)
        elem.clear()
        sleep(1)
        elem.send_keys("kapitan bomba")
        sleep(1)
        elem.send_keys(Keys.RETURN)
        sleep(1)


class LogInTest(StaticLiveServerTestCase):
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def test_someone_can_login(self):
        homepage = Homepage(self.browser)
        homepage.navigate()
        sleep(2)
        signup_form = homepage.getLoginform()
        signup_form.navigate()
        sleep(2)
        signup_form.setUsername("Justin")
        signup_form.setPassword("asdf")
        sleep(2)
        signup_form.submit()
        sleep(2)
        elem = self.browser.find_element_by_css_selector('.alert')
        assert elem is not None

    def tearDown(self):
        self.browser.close()
