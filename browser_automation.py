#!/usr/bin/python3
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
#options = Options()
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
download_dir = "/home/user/Downloads/selenium/"
options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : download_dir}
#options.add_argument("--headless")
options.add_argument("user-data-dir=selenium")
options.add_experimental_option("prefs",prefs)
options.add_experimental_option("detach", True)
service = Service(executable_path="/snap/bin/chromium.chromedriver")
browser = None

ut_moodle_auth = "https://moodle.ut.ee/auth/oidc/"
ut_user = "..."
ut_pass = "..."

def browser_init():
    global browser
    browser = webdriver.Chrome(service=service, options=options)
    browser.set_window_size(1200, 1000)
    browser.set_page_load_timeout(1800)


def login_microsoftonline():

    # check if "pick an account" option available (login session available)
    button = browser.find_element(By.XPATH, ".//div[@class='table']")
    if button and 'arnis@ut.ee' in button.text:
        button.click()
        sleep(2)
    else:


        # submit username
        print("[+] get_oauth2_token(): submitting username...")
        if not browser.find_elements(By.XPATH, ".//input[@name='loginfmt']"):
            print("[-] get_oauth2_token(): login form not found!")
            exit(1)
        form = browser.find_element(By.XPATH, ".//input[@name='loginfmt']")
        form.click()
        form.send_keys(ut_user+'@ut.ee'+Keys.ENTER)
        sleep(2)

    # submit password
    print("[+] get_oauth2_token(): submitting password...")
    if not browser.find_elements(By.XPATH, ".//input[@name='passwd']"):
        print("[-] get_oauth2_token(): password form not found!")
        exit(1)
    form = browser.find_element(By.XPATH, ".//input[@name='passwd']")
    form.click()
    form.send_keys(ut_pass+Keys.ENTER)
    sleep(2)

    # wait for 2nd factor auth code
    print("[+] get_oauth2_token(): looking for 2nd factor auth code...")
    while not browser.find_elements(By.XPATH, ".//div[@class='display-sign-container']") and 'Panopto' not in browser.current_url:
        print("[+] get_oauth2_token(): waiting for 2nd factor auth code...")
        #print(browser.title)
        if 'Moodle' in browser.title or 'ÕIS II' in browser.title: break
        sleep(1)
    while browser.find_elements(By.XPATH, ".//div[@class='display-sign-container']"):
        print("[+] get_oauth2_token(): waiting for confirmation...")
        sleep(1)

def open_moodle_ut():
    if not browser: browser_init()

    print("[+] opening:", ut_moodle_auth)
    browser.get(ut_moodle_auth)
    sleep(2)

    login_microsoftonline()


def open_moodle_course(ut_moodle):
    # open course page
    print("[+] opening:", ut_moodle)
    browser.get(ut_moodle)

    # switch to edit mode
    browser.find_element(By.XPATH, "//a[contains(@href, 'edit=on')]").click()
    sleep(1)

def moodle_grade_attempt_question(attempt_id, nr, score, feedback):
    print("[+] moodle_grade_attempt_question(): %s[%s]: %s (%s)" % (attempt_id, nr, score, feedback))
    browser.get(f"https://moodle.ut.ee/mod/quiz/comment.php?attempt={attempt_id}&slot={nr}")

    while not browser.find_elements(By.XPATH, "//input[@type='text']"):
        sleep(0.2)

    # add mark
    mark = browser.find_element(By.XPATH, "//input[@type='text']")
    mark.clear()
    mark.send_keys(score)

    # add comment
    iframe = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
    browser.switch_to.frame(iframe)
    editor = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "tinymce")))
    browser.execute_script("arguments[0].focus();", editor)
    browser.execute_script("arguments[0].innerHTML = '';", editor)
    editor.send_keys(feedback)
    browser.switch_to.default_content()

    # click 'Save'
    browser.find_element(By.ID, "id_submitbutton").click()

    # wait until response loads
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-close")))
    return

