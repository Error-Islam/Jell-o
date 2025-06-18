from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

url = "https://xn2f4k-8080.csb.app/auth/login"

def run_bot():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    time.sleep(5)
    try:
        btn = driver.find_element(By.XPATH, "//button[contains(text(),'Yes, proceed')]")
        btn.click()
    except Exception as e:
        print("Button not found:", e)

    time.sleep(14 * 60)  # Wait for 14 mins
    driver.quit()

while True:
    run_bot()
  
