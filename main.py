from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Facebook credentials (replace these with your actual email and password)
FB_EMAIL = "YOUR_FACEBOOK_EMAIL"
FB_PASSWORD = "YOUR_FACEBOOK_PASSWORD"

# Initialize Chrome driver
driver = webdriver.Chrome()

# Open Tinder homepage
driver.get("https://www.tinder.com")

# Explicit wait
wait = WebDriverWait(driver, 10)

try:
    # Click on the 'Log in' button
    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Log in")]')))
    login_btn.click()

    # Choose login via Facebook
    fb_login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Log in with Facebook")]')))
    fb_login_btn.click()

    # Switch to Facebook login window
    main_window = driver.current_window_handle
    driver.switch_to.window(driver.window_handles[1])

    # Facebook login process
    email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
    pass_input = driver.find_element(By.ID, "pass")

    email_input.send_keys(FB_EMAIL)
    pass_input.send_keys(FB_PASSWORD)
    pass_input.send_keys(Keys.ENTER)

    # Switch back to Tinder window
    driver.switch_to.window(main_window)

    # Handle permissions popups
    try:
        allow_location_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Allow")]')))
        allow_location_btn.click()
    except TimeoutException:
        print("Location permission popup not shown.")

    try:
        disable_notifications_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not interested")]')))
        disable_notifications_btn.click()
    except TimeoutException:
        print("Notification permission popup not shown.")

    # Accept cookies if present
    try:
        cookies_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "I accept")]')))
        cookies_btn.click()
    except TimeoutException:
        print("Cookies popup not shown.")

    # Start liking profiles
    for i in range(50):  # Reduced to 50 likes for safety, adjust as needed
        sleep(1)  # Delay to mimic human behavior

        try:
            like_btn = driver.find_element(By.XPATH, '//button[@aria-label="Like"]')
            like_btn.click()
            print(f"Liked profile {i + 1}")

        except ElementClickInterceptedException:
            print("Like button blocked, handling popup...")
            try:
                # Handle match popup if it appears
                match_popup = driver.find_element(By.CSS_SELECTOR, '.itsAMatch a')
                match_popup.click()
                print("Closed match popup.")
            except NoSuchElementException:
                print("No match popup found.")
                sleep(2)  # Wait before retrying
        except NoSuchElementException:
            print("Like button not found, waiting...")
            sleep(2)  # Wait before retrying

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close browser session
    driver.quit()
    print("Session ended.")
