from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time
import re

print("📌 Script started...")

# Setup path to chromedriver
driver_path = r"C:\Users\acer\Desktop\College\DevOps\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Base folder path for all HTML files
base_path = r"C:\Users\acer\Desktop\College\DevOps"

# Load index.html first
index_path = f"file:///{os.path.join(base_path, 'index.html').replace(os.sep, '/')}"
print("🌐 Opening index.html page...")
driver.get(index_path)
driver.maximize_window()
time.sleep(2)  # Give it time to load

# Portfolio page names to test
portfolio_pages = [
    "Renees.html",
    "Jebisha.html",
    "Rathnaa.html",
    "Shyma.html",
    "Stefflin.html"
]

# Function to run test cases on a given portfolio page
def test_portfolio(page_name):
    full_path = f"file:///{os.path.join(base_path, page_name).replace(os.sep, '/')}"
    print(f"\n📄 Opening portfolio: {page_name}")
    driver.get(full_path)
    time.sleep(1)

    print(f"🔍 Testing: {page_name}")

    # 1. ✅ Image presence
    images = driver.find_elements(By.TAG_NAME, "img")
    print("✅ Image(s) found." if images else "❌ No images found.")

    # 2. ✅ Name presence (h1, h2, or class='name')
    try:
        name = driver.find_element(By.XPATH, "//h1 | //h2 | //*[@class='name']")
        print(f"✅ Name found: {name.text}")
    except:
        print("❌ Name not found.")

    # 3. ✅ Any number (e.g., phone, age)
    page_text = driver.find_element(By.TAG_NAME, "body").text
    numbers = re.findall(r'\d+', page_text)
    print(f"✅ Numbers found: {numbers}" if numbers else "❌ No numbers found.")

    # 4. ✅ Background image check (inline CSS)
    body_style = driver.find_element(By.TAG_NAME, "body").get_attribute("style")
    print("✅ Background image found in inline style." if 'background-image' in body_style else "❌ No background image in inline style.")

    # 5. ✅ Email and project repo link check
    links = driver.find_elements(By.TAG_NAME, "a")
    email_found = any("mailto:" in link.get_attribute("href") for link in links if link.get_attribute("href"))
    repo_found = any(("github.com" in link.get_attribute("href") or "gitlab.com" in link.get_attribute("href")) for link in links if link.get_attribute("href"))

    print("✅ Email found." if email_found else "❌ Email not found.")
    print("✅ Project repo link found." if repo_found else "❌ Project repo link not found.")

# Run tests for each portfolio page
for page in portfolio_pages:
    test_portfolio(page)

# Close browser
driver.quit()
print("\n🏁 Script ended.")
