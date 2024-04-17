import pytest
import ssl
import undetected_chromedriver as uc
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Set user credentials and website URL
email = "ffffff@gmail.com"
password = "12345678"
website = "http://earnaha.com/"

# Ignore SSL verification warning
ssl._create_default_https_context = ssl._create_unverified_context


# Define browser fixture
@pytest.fixture(scope="module")
def browser():
    driver = uc.Chrome()
    driver.delete_all_cookies()
    yield driver
    driver.quit()


# Test case description: Test sign in functionality with email
def test_sign_in_with_email(browser):
    browser.get(website)

    # Find and click on sign-in button
    try:
        sign_in_button = WebDriverWait(browser, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, ".outlined-dark---log-in.w-button"))
        )
        sign_in_button.click()
    except (NoSuchElementException, TimeoutException) as e:
        pytest.fail(f"Sign-in button not found: {e}")

    # Input email information
    email_input = browser.find_element(by=By.NAME, value="username")
    email_input.send_keys(email)

    # Input password information and submit the form
    password_input = browser.find_element(by=By.NAME, value="password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

    # Wait for sign-in result
    sign_in_failure = WebDriverWait(browser, 10).until(
        ec.presence_of_element_located((By.ID, "error-element-password"))
    )
    if sign_in_failure.is_displayed():
        print("User login failed.")
    else:
        print("User successfully logged in!")


# Test case description: Test sign in functionality with Google OAuth
def test_sign_in_with_google_oauth(browser):
    browser.get(website)

    # Find and click the sign-in button
    try:
        sign_in_button = WebDriverWait(browser, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, ".outlined-dark---log-in.w-button"))
        )
        sign_in_button.click()
    except (NoSuchElementException, TimeoutException) as e:
        pytest.fail(f"Sign-in button not found: {e}")

    # Click on sign-in with Google button
    try:
        sign_in_button_google = WebDriverWait(browser, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, ".c4781712b.cbbdcb01f.c41cf6d0d"))
        )
        sign_in_button_google.click()
    except (NoSuchElementException, TimeoutException) as e:
        pytest.fail(f"Sign-in button not found: {e}")

    # Input Google email information
    email_input = browser.find_element(by=By.NAME, value="identifier")
    email_input.send_keys(email)
    email_input.send_keys(Keys.ENTER)

    # Wait for password input box and input password information
    password_input = WebDriverWait(browser, 10).until(
        ec.element_to_be_clickable((By.NAME, "Passwd"))
    )
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

    # Wait for sign-in result
    sign_in_failure = WebDriverWait(browser, 10).until(
        ec.presence_of_element_located((By.XPATH, "//h1[contains(text(), '504 ERROR')]"))
    )
    if sign_in_failure.is_displayed():
        print("User login failed.")
    else:
        print("User successfully logged in!")
