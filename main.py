from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
import os

# === Configuration ===
LOGIN_URL = "https://hlykv5-8080.csb.app"
EMAIL = "Visitor@jello.org"
PASSWORD = "Visitor"
COOKIES_FILE = "cookies.pkl"
REFRESH_INTERVAL = 60  # seconds
TOTAL_MINUTES = 60  # how long to run the bot

def save_cookies(driver, path):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
        print("✅ Cookies saved")

def load_cookies(driver, path):
    with open(path, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        print("✅ Cookies loaded")

def is_logged_in(driver):
    # Check for something that only appears when logged in
    return "dashboard" in driver.current_url or "auth/login" not in driver.current_url

def perform_login(driver):
    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
        )
        password_input = driver.find_element(By.XPATH, "//input[@type='password']")
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign in')]")

        email_input.clear()
        email_input.send_keys(EMAIL)
        password_input.clear()
        password_input.send_keys(PASSWORD)
        login_button.click()

        # Wait until redirected or dashboard loaded
        WebDriverWait(driver, 10).until(lambda d: is_logged_in(d))
        print("🔓 Logged in successfully")
        save_cookies(driver, COOKIES_FILE)
    except Exception as e:
        print(f"❌ Login failed: {e}")

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(LOGIN_URL)
    print(f"🌐 Opened {LOGIN_URL}")

    # Try loading cookies
    if os.path.exists(COOKIES_FILE):
        try:
            load_cookies(driver, COOKIES_FILE)
            driver.refresh()
            time.sleep(3)
            if is_logged_in(driver):
                print("🔓 Logged in using saved session")
            else:
                print("🔐 Session expired, performing login")
                perform_login(driver)
        except Exception as e:
            print(f"⚠️ Failed loading cookies: {e}")
            perform_login(driver)
    else:
        perform_login(driver)

    # Auto-refresh every minute
    start_time = time.time()
    while (time.time() - start_time) < TOTAL_MINUTES * 60:
        time.sleep(REFRESH_INTERVAL)
        driver.refresh()
        print(f"🔁 Page refreshed at {time.strftime('%H:%M:%S')}")

    driver.quit()
    print("🧹 Bot finished and browser closed")

if __name__ == "__main__":
    main()
