from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

class Logintest(LiveServerTestCase):
    def setUp(self):
        service = Service(r'D:\mca\geckodriver.exe')
        self.driver = webdriver.Firefox(service=service)
        self.driver.implicitly_wait(10)
        self.live_server_url = "http://127.0.0.1:8000/login"  # Updated URL

    def tearDown(self):
        self.driver.quit()

    def fill_form(self, username='', password=''):
        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        driver.find_element(By.ID, "username").send_keys(username)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        driver.find_element(By.ID, "password").send_keys(password)

    def test_correct_credentials(self):
        self.driver.get(self.live_server_url)
        self.fill_form(username="admin", password="admin")
        self.driver.find_element(By.ID, "testid").click()
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.dismiss()  # Dismiss the alert
            self.fail(f"Login attempt failed with alert: {alert_text}")
        except TimeoutException:
            # No alert, continue with the test
            pass
        self.assertIn("dashboard/", self.driver.current_url)
        print("Test scenario 'View Users' passed.")

    def test_complaint_list_page(self):
        complaint_list_url = self.live_server_url + 'http://127.0.0.1:8000/complaints/'  # Change to your actual complaint list page URL

        # Log in with valid credentials
        self.driver.get(self.live_server_url)
        self.fill_form(username="admin", password="admin")
        self.driver.find_element(By.ID, "testid").click()

        # Navigate to the complaint list page
        self.driver.get(complaint_list_url)

        # Check if the title is "Complaint List"
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Complaints")
        )


        print("Test scenario 'Complaint List Page' passed.")

if __name__ == '__main__':
    LiveServerTestCase.main()
