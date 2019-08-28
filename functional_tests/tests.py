from selenium import webdriver
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
import time
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 3

class FirstFunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, fn, *args, **kwargs):
        start_time = time.time()
        while True:
            try:
                result = fn(*args, **kwargs)
                return result
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_home_page_prompts_for_username_and_takes_user_to_his_url(self):
        # go to home page
        self.browser.get(self.live_server_url)

        # notices home page says Fred and Fred
        self.assertIn('Fred and Fred', self.browser.title)

        # user sees box to sign in
        inputbox = self.browser.find_element_by_id('username')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter username'
        )

        # after submitting name, user is directed to personal page with his url
        inputbox.send_keys('andrew')
        inputbox.send_keys(Keys.ENTER)
        andrew_url = self.browser.current_url
        self.assertRegex(andrew_url, '/andrew.+')




        