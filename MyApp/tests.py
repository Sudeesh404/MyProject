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
        self.fill_form(username="sudeesh43", password="sushi@123")
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
        self.assertIn("user_landing/", self.driver.current_url)
        print("Test scenario 'Users Login' passed.")
        print("Test scenario 'File Complaint' passed.")

    def test_file_complaint(self):
        complaint_url = f"{self.live_server_url}/file_complaint/"  
        self.driver.get(complaint_url)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "name"))
            )
        except TimeoutException as e:
            print(f"TimeoutException: {e}")
            print(f"Current URL: {self.driver.current_url}")
            print(f"Current Title: {self.driver.title}")
            raise
        try:
            name_input = self.driver.find_element(By.ID, "name")
            place_input = self.driver.find_element(By.NAME, "place")
            description_input = self.driver.find_element(By.NAME, "Description")

            # Fill out the form with sample data
            name_input.send_keys("John Doe")
            place_input.send_keys("Sample Place")
            description_input.send_keys("This is a test complaint.")

            # Submit the form
            submit_button = self.driver.find_element(By.ID, "submitButton")
            submit_button.click()

            # Wait for the success message or redirect
            WebDriverWait(self.driver, 10).until(
                EC.url_matches("/success_page/")  # Adjust the URL or success condition accordingly
            )

            # Assert success (You can customize this based on your application behavior)
            self.assertIn("success", self.driver.current_url)
            self.assertEqual("Complaint submitted successfully!", self.driver.find_element(By.ID, "successMessage").text)

        except NoSuchElementException as e:
            print(f"NoSuchElementException: {e}")
            print(f"Current URL: {self.driver.current_url}")
            print(f"Current Title: {self.driver.title}")
            raise

        print("Test scenario 'File Complaint' passed.")

if __name__ == '__main__':
    LiveServerTestCase.main()
