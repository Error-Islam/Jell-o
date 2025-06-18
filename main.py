from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

url = "https://xn2f4k-8080.csb.app/auth/login"

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

time.sleep(5)  # Wait for page to load

try:
    # Click the "Yes, proceed..." button
    proceed_button = driver.find_element(By.XPATH, "//button[contains(text(),'Yes, proceed')]")
    proceed_button.click()
    print("Clicked the proceed button.")
except Exception as e:
    print("Proceed button not found or error:", e)

# Stay for 14 minutes with refreshes every 5 minutes
total_minutes = 14
refresh_interval = 5

elapsed = 0
while elapsed < total_minutes:
    print(f"Elapsed: {elapsed} min — sleeping for {refresh_interval} more...")
    time.sleep(refresh_interval * 60)
    elapsed += refresh_interval
    if elapsed < total_minutes:
        print("Refreshing the page...")
        driver.refresh()
        time.sleep(5)  # Give time to reload

print("Time complete. Closing browser.")
driver.quit()
