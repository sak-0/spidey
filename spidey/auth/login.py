from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import argparse

parser = argparse.ArgumentParser(description='Login script')
parser.add_argument('--rep-type', choices=['extrahealth', 'eh', 'enrollprime', 'nuera'], help='Type of representative')
parser.add_argument('--url', choices=['rep', 'group', 'member'], help='Dashboard URL')
args = parser.parse_args()

load_dotenv(dotenv_path=".env", override=True)

rep_type_map = {
    "extrahealth": "ENROLL_REP_EMAIL",
    "eh": "ENROLL_REP_EMAIL",
    "enrollprime": "ENROLL_REP_EMAIL",
    "nuera": "NUERA_REP_EMAIL"
}

url_map = {
    "rep": "QA_REP_URL",
    "group": "QA_GROUP_URL",
    "member": "QA_MEMBER_URL"
}

if args.url:
    url_env_var = url_map[args.url]
    dashboard_url = os.getenv(url_env_var)

if args.rep_type:
    rep_type_env_var = rep_type_map[args.rep_type]
    rep_type_email = os.getenv(rep_type_env_var)
    rep_password = os.getenv("REP_PASSWORD")

default_otp = os.getenv("DEFAULT_OTP")



def login():
    # Check if the proxy server is accessible
    try:
        response = os.system("curl -x http://localhost:1337 http://example.com")
        if response != 0:
            raise Exception("Proxy server is not accessible. Please check the proxy configuration.")
    except Exception as e:
        print(f"Proxy check failed: {e}")
        return

    chrome_options = Options()
    chrome_options.add_argument('--proxy-server=http://localhost:1337')
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(dashboard_url)
        time.sleep(2)
        print("Login page loaded")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Email")))
        email_field = driver.find_element(By.ID, "Email")
        print(email_field)

        if args.url == "rep":
            email_field.send_keys(rep_type_email)
        elif args.url == "group":
            email_field.send_keys(os.getenv("QA_GRP_EMAIL"))
        elif args.url == "member":
            email_field.send_keys(os.getenv("QA_MEM_EMAIL"))
        
        next_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        next_button.click()
        
        time.sleep(2)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))

        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        if args.url == "rep":
            password_field.send_keys(rep_password)
        elif args.url == "group":
            password_field.send_keys(os.getenv("QA_GRP_PASSWORD"))
        elif args.url == "member":
            password_field.send_keys(os.getenv("QA_MEM_PASSWORD"))
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        time.sleep(5)

        # if /login-otp is not the current url, then redirect to /login-otp
        if args.url == "rep":
            if not driver.current_url.endswith("login-otp"):
                driver.get(f"{dashboard_url}login-otp")
                time.sleep(2)
        
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".otp-input-wrapper input[type='tel']")))

        otp_fields = driver.find_elements(By.CSS_SELECTOR, ".otp-input-wrapper input[type='tel']")
        print(f"Found {len(otp_fields)} OTP fields.")
        if len(otp_fields) == 6:
            # Try default OTP first
            for i, otp_digit in enumerate(default_otp):
                if args.rep_type == "extrahealth" or args.rep_type == "eh" or args.rep_type == "enrollprime":
                    otp_fields[i].send_keys(otp_digit)
                    
            correct_otp = input("Enter the correct OTP: ")

            for i, otp_digit in enumerate(correct_otp):
                otp_fields[i].clear()
                otp_fields[i].send_keys(otp_digit)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # driver.quit()
        print("Login successful")

if __name__ == "__main__":
    login()
    # Keep the browser open
    time.sleep(999999999)
