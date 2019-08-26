from selenium import webdriver
from django.contrib.staticfiles.testing import LiveServerTestCase


class FirstFunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_if_django_browser_will_open(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Django', self.browser.page_source)
        