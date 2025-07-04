from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time
import sys

def run_session(total_minutes=60, refresh_interval=0.5):  # 0.5 minutes = 30 seconds
    url = "https://26p6pg-8080.csb.app"
    
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
            print("Session completed - Browser closed successfully")
        except:
            pass

def main():
    while True:  # Infinite outer loop
        print("\n" + "="*50)
        print("Starting new monitoring session")
        print("="*50 + "\n")
        
        run_session(total_minutes=60, refresh_interval=0.5)  # 30 second intervals for 60 minutes
        
        # Optional: add a small delay between sessions if needed
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript stopped by user")
        sys.exit(0)
