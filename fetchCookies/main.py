from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(f"user-data-dir={CHROME_USER_DATA_DIR}")
chrome_options.add_argument("--remote-debugging-port=9222")

service = Service(ChromeDriverManager(version="131.0.6778.204").install())

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

time.sleep(5)

cookies = driver.get_cookies()
cookie_file_path = "/root/.config/chromium/cookies.pkl"
with open(cookie_file_path, 'wb') as cookie_file:
    pickle.dump(cookies, cookie_file)

driver.quit()

print(f"Cookies have been saved to {cookie_file_path}")
