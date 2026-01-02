import datetime
import json
import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# --- AUTOMATIC PATH CONFIGURATION ---
# This ensures the JSON is always in the same folder as the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIRTHDAYS_FILE = os.path.join(BASE_DIR, "birthdays.json")

# Update this to your actual Chrome profile path
CHROME_USER_DATA_PATH = r"C:\Users\HP\OneDrive\Desktop\Pyhton\ChromeProfile"

# --- AUTOMATED MESSAGE LIST ---
def get_random_wish(name):
    first_name = name.split()[0]
    messages = [
        f"Happy Birthday {first_name}! 🎂🎉 Hope you have an amazing day!",
        f"Wishing you a very Happy Birthday, {first_name}! 🎈 Enjoy your special day!",
        f"Happy Birthday {first_name}! ✨ May this year be your best one yet!",
        f"Hey {first_name}, Happy Birthday! 🥳 Have a blast today!",
        f"Many happy returns of the day, {first_name}! 🎊🎂"
    ]
    return random.choice(messages)

# --- DATABASE LOGIC ---
def setup_json():
    if not os.path.exists(BIRTHDAYS_FILE):
        with open(BIRTHDAYS_FILE, "w") as f:
            json.dump([], f)
        print(f"✅ Created new database at: {BIRTHDAYS_FILE}")

def manage_birthdays():
    setup_json()
    if input("Manage birthdays? (y/n): ").lower() != 'y':
        return
    with open(BIRTHDAYS_FILE, "r") as f:
        data = json.load(f)
    while True:
        name = input("Contact Name (Exact WhatsApp name): ").strip()
        if not name: break
        d = input("Day (1-31): ").strip()
        m = input("Month (1-12): ").strip()
        data.append({"name": name, "birth_date": d, "birth_month": m})
        if input("Add another? (y/n): ").lower() != 'y': break
    with open(BIRTHDAYS_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def get_today_list():
    today = datetime.datetime.now()
    d, m = str(today.day), str(today.month)
    names = []
    if os.path.exists(BIRTHDAYS_FILE):
        with open(BIRTHDAYS_FILE, "r", encoding='utf-8') as f:
            for person in json.load(f):
                if str(person["birth_date"]) == d and str(person["birth_month"]) == m:
                    names.append(person["name"])
    return names

# --- BOT LOGIC ---
def run_bot(name_list):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={CHROME_USER_DATA_PATH}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://web.whatsapp.com/")
        wait = WebDriverWait(driver, 60)
        
        print("⏳ Waiting for WhatsApp Web to load...")
        # Target the search/textbox specifically in the side panel
        search_xpath = '//div[@contenteditable="true"][@role="textbox"]'
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, search_xpath)))

        for name in name_list:
            try:
                print(f"🔍 Processing: {name}")
                
                # 1. Search for contact
                search_box.click()
                search_box.send_keys(Keys.CONTROL + "a")
                search_box.send_keys(Keys.BACKSPACE)
                time.sleep(1)
                for char in name:
                    search_box.send_keys(char)
                time.sleep(3)

                # 2. Click the contact
                contact_xpath = f'//span[@title="{name}"]'
                contact_btn = wait.until(EC.element_to_be_clickable((By.XPATH, contact_xpath)))
                contact_btn.click()
                time.sleep(2)

                # 3. Message Delivery with Deep Focus
                msg_box_xpath = '//footer//div[@contenteditable="true"][@role="textbox"]'
                msg_box = wait.until(EC.presence_of_element_located((By.XPATH, msg_box_xpath)))
                
                # Click the box to ensure focus
                actions = ActionChains(driver)
                actions.move_to_element(msg_box).click().perform()
                time.sleep(1)
                
                message = get_random_wish(name)
                # Type message character by character
                for char in message:
                    msg_box.send_keys(char)
                
                time.sleep(1)
                msg_box.send_keys(Keys.ENTER)
                
                print(f"✅ Automated message delivered to {name}")
                time.sleep(3)

            except Exception as e:
                print(f"❌ Failed to deliver to '{name}'. Skipping...")
                driver.get("https://web.whatsapp.com/")
                time.sleep(5)

    except Exception as e:
        print(f"🛑 Bot Error: {e}")
    finally:
        if driver:
            print("Closing browser...")
            time.sleep(5)
            driver.quit()

# --- EXECUTION ---
if __name__ == "__main__":
    manage_birthdays()
    today_wishes = get_today_list()
    
    if today_wishes:
        print(f"🎂 Today's Birthdays: {today_wishes}")
        run_bot(today_wishes)
    else:
        print("📭 No birthdays found for today.")