from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time
import sys
import os
import psutil
from datetime import datetime

def is_script_already_running():
    """Check if another instance of this script is running"""
    current_pid = os.getpid()
    script_name = os.path.basename(__file__)
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if (proc.info['name'] in ['python', 'python3'] and 
                len(proc.info['cmdline']) > 1 and 
                script_name in proc.info['cmdline'][1] and 
                proc.info['pid'] != current_pid):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, IndexError):
            continue
    return False

def run_session(total_minutes=60, refresh_interval=0.5):
    url = "https://26p6pg-8080.csb.app"
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Successfully navigated to {url}")
        
        # Initial button click attempt
        try:
            proceed_button = driver.find_element(By.XPATH, "//button[contains(text(),'Yes, proceed')]")
            proceed_button.click()
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Clicked 'Yes, proceed' button")
        except NoSuchElementException:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Proceed button not found")
        
        # Main refresh loop
        start_time = time.time()
        while (time.time() - start_time) < total_minutes * 60:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            elapsed = (time.time() - start_time) / 60  # in minutes
            print(f"{current_time} - Elapsed: {elapsed:.1f} minutes")
            
            try:
                driver.refresh()
                print(f"{current_time} - Page refreshed")
            except WebDriverException as e:
                print(f"{current_time} - Refresh error: {str(e)}")
                try:
                    driver.quit()
                    driver = webdriver.Chrome(options=chrome_options)
                    driver.get(url)
                    print(f"{current_time} - Recovered by restarting driver")
                except Exception as recovery_error:
                    print(f"{current_time} - Recovery failed: {str(recovery_error)}")
                    break
            
            time.sleep(refresh_interval * 60)
            
    except Exception as main_error:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Fatal error: {str(main_error)}")
    finally:
        if driver:
            try:
                driver.quit()
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Browser closed successfully")
            except:
                pass

def main():
    if is_script_already_running():
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Another instance is already running. Exiting.")
        sys.exit(0)
    
    while True:
        print("\n" + "="*50)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting new monitoring session")
        print("="*50 + "\n")
        
        run_session(total_minutes=60, refresh_interval=0.5)
        
        # Wait between 6-7 hours before next session
        wait_time = 6 * 3600 + random.randint(0, 3600)  # 6-7 hours in seconds
        next_run = datetime.now() + timedelta(seconds=wait_time)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Next session at: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(wait_time)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Script stopped by user")
        sys.exit(0)
