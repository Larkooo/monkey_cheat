from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import random
import string

import time
import os

from dotenv import load_dotenv
load_dotenv()

# verbosity
load_dotenv(verbose=True)

from pathlib import Path  # dont import if your python version is under 3.6
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

driver = webdriver.Chrome()
driver.get("https://monkeytype.com/login")
time.sleep(1)

#Enter login infos

email = driver.find_element_by_xpath("//input[@autocomplete='email']")
password = driver.find_element_by_xpath("//input[@autocomplete='password']")
login = driver.find_element_by_xpath("//div[@class='login side']")
signin = login.find_element_by_class_name("button")

email.send_keys(os.getenv("EMAIL"))

time.sleep(2)

password.send_keys(os.getenv("PASSWORD"))

time.sleep(1)

signin.click()

alphabet_string = list(string.ascii_lowercase)

time.sleep(2)


timeconfig = driver.find_element_by_xpath(f"//div[@timeconfig=" + "'" + os.getenv("TIME_CONFIG") + "'" + "]").click()

time.sleep(1)

# Start checking words
words_div = driver.find_element_by_id("words")
typingTest = driver.find_element_by_id("wordsInput")

time.sleep(1)

while True:
    try:
        active_word = words_div.find_element_by_xpath("//div[@class='word active']")

        letters = ""
        for letter in active_word.find_elements_by_xpath(".//letter"):
            #try:
            #    typingTest.send_keys(letter.text)
            #except Exception:
            #    pass
            letters += letter.text
        for letter in letters:
            if random.randint(0, 100) <= 1:
                typingTest.send_keys(random.choice(alphabet_string))
            elif random.randint(0, 100) < 5:
                typingTest.send_keys(random.choice(alphabet_string))
                time.sleep(random.random() / random.randint(5, 8))
                typingTest.send_keys(Keys.BACKSPACE)
                time.sleep(random.random() / random.randint(7, 9))
                typingTest.send_keys(letter)
            else:
                typingTest.send_keys(letter)
            time.sleep(random.random() / random.randint(8, 15))
        typingTest.send_keys(" ")
    except Exception:
        break


wpm = driver.find_element_by_xpath("//div[@class='group wpm']")
acc = driver.find_element_by_xpath("//div[@class='group acc']")

wpm_value = wpm.find_element_by_class_name("bottom").get_attribute("aria-label")
acc_value = acc.find_element_by_class_name("bottom").get_attribute("aria-label")

print(f"""
WPM = {wpm_value}
ACCURACY = {acc_value}
""")

driver.close()