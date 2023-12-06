from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class LoginSeleniumTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_with_valid_credentials(self):
        self.live_server_url='http://127.0.0.1:8000/'
        self.selenium.get(self.live_server_url + 'login/')  # Update with your login URL

        # Replace 'your_username' and 'your_password' with valid credentials
        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        username_input.send_keys('vishnu')
        password_input.send_keys('vV@12345')
        self.selenium.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()


        # Wait for the page to load after clicking submit
        self.selenium.implicitly_wait(5)  # Adjust the time based on your application behavior

        # Example assertions based on your application behavior
        # Uncomment and modify according to your actual HTML structure and expected results
        # self.assertIn('Welcome', self.selenium.page_source)
        # self.assertIn('Dashboard', self.selenium.title)
        # self.assertTrue(self.selenium.find_element_by_css_selector('.user-welcome').is_displayed())

        # Optionally, add a sleep to keep the browser open for a moment (for manual inspection)
        # time.sleep(5)
