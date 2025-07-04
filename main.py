from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def main():
    url = "https://26p6pg-8080.csb.app"
    total_minutes = 60  # total run time
    refresh_interval = 30  # seconds

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    print(f"Opened {url}")

    # Try to click the 'Yes, proceed' button once at start
    try:
        button = driver.find_element(By.XPATH, "//button[contains(text(),'Yes, proceed')]")
        button.click()
        print("Clicked 'Yes, proceed' button")
    except NoSuchElementException:
        print("'Yes, proceed' button not found")

    start_time = time.time()
    while (time.time() - start_time) < total_minutes * 60:
        time.sleep(refresh_interval)
        driver.refresh()
        print(f"Refreshed page at {time.strftime('%H:%M:%S')}")

    driver.quit()
    print("Bot finished and browser closed")

if __name__ == "__main__":
    main()
