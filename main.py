from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time
import sys

def main():
    url = "https://yvzd8f-8080.csb.app"
    total_minutes = 480  # 8 hours total runtime
    refresh_interval = 1  # Refresh every 1 minute (adjust as needed)

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        print(f"Successfully navigated to {url}")
        
        # Initial button click attempt
        try:
            proceed_button = driver.find_element(By.XPATH, "//button[contains(text(),'Yes, proceed')]")
            proceed_button.click()
            print("Successfully clicked the 'Yes, proceed' button")
        except NoSuchElementException:
            print("Proceed button not found - may have already been clicked or not present")
        
        # Main refresh loop
        elapsed = 0
        while elapsed < total_minutes:
            print(f"Elapsed: {elapsed} minutes - Next refresh in {refresh_interval} minute(s)")
            time.sleep(refresh_interval * 60)
            elapsed += refresh_interval
            
            try:
                driver.refresh()
                print(f"Page refreshed at {time.strftime('%H:%M:%S')}")
            except WebDriverException as e:
                print(f"Error refreshing page: {e}")
                # Try to recover by restarting the driver
                try:
                    driver.quit()
                    driver = webdriver.Chrome(options=chrome_options)
                    driver.get(url)
                    print("Recovered by restarting driver")
                except Exception as recovery_error:
                    print(f"Recovery failed: {recovery_error}")
                    break
        
    except Exception as main_error:
        print(f"Fatal error: {main_error}")
    finally:
        try:
            driver.quit()
            print("Browser closed successfully")
        except:
            pass
        sys.exit()

if __name__ == "__main__":
    main()
