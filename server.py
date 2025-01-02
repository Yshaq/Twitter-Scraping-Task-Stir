from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By

import zipfile

from pymongo import MongoClient
from datetime import datetime
import pytz
import os

load_dotenv()  # take environment variables from .env.


app = Flask(__name__)
CORS(app) 

USE_PROXY = os.getenv('USE_PROXY', 0)
PROXY_HOST = os.getenv('PROXY_HOST')  # rotating proxy
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_USER = os.getenv('PROXY_USER')
PROXY_PASS = os.getenv('PROXY_PASS')
MONGODB_URI = os.getenv('MONGODB_URI')
TWITTER_EMAIL = os.getenv('TWITTER_EMAIL')
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

USE_PROXY = int(USE_PROXY)

uri = MONGODB_URI
client = MongoClient(uri)
db = client.stir_scrape
twitter_collection = db.twitter_data

# Using Proxy
def get_proxy_chrome_driver(use_proxy=False, user_agent=None):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    service = Service(executable_path='./chromedriver')
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)

    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options)
    return driver


# No Proxy
def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(executable_path='./chromedriver')
                              , options=options
                            )
    return driver
    

def scrape():
    print("Flow Start!")
    if USE_PROXY:
        print("Using Proxy!")
        driver = get_proxy_chrome_driver(use_proxy=True)
    else:
        print("Not Using Proxy")
        driver = get_chrome_driver()

    wait = WebDriverWait(driver, 20)

    print("Getting IP")

    driver.get("https://api.ipify.org")
    ip_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'pre')))
    ip = ip_element.text
    print("IP is", ip)

    print("Starting Scrape!")
    driver.get("https://x.com/login")

    input_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    input_element.send_keys(TWITTER_EMAIL)

    next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Next']")))

    next_button.click()
    print("Email Flow Done")

    input_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input')))

    if "Enter your phone number or username" in driver.page_source:
        print("Asked for username Confirmation!")
        input_element.send_keys(TWITTER_USERNAME)  

        next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Next']")))
        next_button.click()
        print("Username Confirmation Done")


    input_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="current-password"]')))
    input_element.send_keys(TWITTER_PASSWORD)

    login_button = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Log in']")))

    login_button.click()
    print("Logging In!")

    time.sleep(3)
    # home_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Home timeline"]')))

    driver.get("https://x.com/explore/tabs/trending")
    explore_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Timeline: Explore"]')))
    time.sleep(2)
    print("Trending Page Loaded!")

    tags = []

    lines = explore_div.text.split('\n')

    curr = 1

    for i in range(len(lines)):
        line = lines[i]
        if line == str(curr):
            tags.append(lines[i+3])
            curr+=1
        if curr>5:
            break

    print(tags)
    driver.quit()
    return ip, tags


@app.route("/")
def index():

    # # Mock response for testing
    # return {
    # "_id": "6775a501c3626fe9bbca5cb8",
    # "ip": "103.151.209.250",
    # "nameoftrend1": "Happy New Year",
    # "nameoftrend2": "#Welcome2025",
    # "nameoftrend3": "#नववर्ष_2025",
    # "nameoftrend4": "Happy 2025",
    # "nameoftrend5": "#ForFairFuture",
    # "timestamp": "2025-01-02 01:56:41"
    # }

    ip, top_5_tags = scrape()
    # Indian timezone
    ist = pytz.timezone("Asia/Kolkata")

    # Get current time in IST
    current_time_ist = datetime.now(ist)

    data = {
        "timestamp": current_time_ist,
        "ip": ip,
        "nameoftrend1": top_5_tags[0],
        "nameoftrend2": top_5_tags[1],
        "nameoftrend3": top_5_tags[2],
        "nameoftrend4": top_5_tags[3],
        "nameoftrend5": top_5_tags[4],
    }

    response = twitter_collection.insert_one(data)

    data['_id']=str(response.inserted_id)
    data['timestamp']=current_time_ist.strftime("%Y-%m-%d %H:%M:%S")
    
    return data

