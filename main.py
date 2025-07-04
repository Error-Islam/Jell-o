from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time
import sys

def main():
    url = "https://26p6pg-8080.csb.app"
    total_minutes = 60  # Total runtime in minutes
    refresh_interval = 0.5  # Refresh every 30 seconds (0.5 minutes)

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
        while elapsed < total_minutes * 60:  # Convert to seconds
            print(f"Elapsed: {elapsed//60} minutes {elapsed%60} seconds - Next refresh in {refresh_interval*60} seconds")
            
            # Check for loader page
            try:
                loader = driver.find_element(By.XPATH, "//*[contains(text(),'Loading') or contains(text(),'Please wait')]")
                print("Loader page detected - waiting...")
                time.sleep(5)  # Wait extra time if loader is present
            except NoSuchElementException:
                pass  # No loader found
            
            time.sleep(refresh_interval * 60)
            elapsed += refresh_interval * 60
            
            try:
                driver.refresh()
                print(f"Page refreshed at {time.strftime('%H:%M:%S')}")
                
                # Handle any post-refresh popups
                try:
                    popup = driver.find_element(By.XPATH, "//button[contains(text(),'OK') or contains(text(),'Accept')]")
                    popup.click()
                    print("Closed popup after refresh")
                except NoSuchElementException:
                    pass
                    
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
