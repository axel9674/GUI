import datetime
import time
from threading import *

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

DISCONNECTED_MSG = 'Unable to evaluate script: disconnected: not connected to DevTools\n'
threadEvent = Event()
threads = []


def check_exists_by(by, xpath, driver):
    try:
        driver.find_element(by, xpath)
    except NoSuchElementException:
        return False
    return True


def login(character):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    if threadEvent.is_set():
        return
    # driver.set_window_position(2560, 0)  # apre la finestra nel secondo schermo
    driver.maximize_window()  # finestra fullscreen
    if threadEvent.is_set():
        return
    driver.get('https://it.battleknight.gameforge.com/')

    if threadEvent.is_set():
        return

    driver.find_element(By.XPATH, '//*[@id="signUpLoginForm"]/div/label[2]').click()

    if threadEvent.is_set():
        return

    time.sleep(1)

    if threadEvent.is_set():
        return

    driver.find_element(By.XPATH, '//*[@id="loginUsername"]').send_keys(character.user)

    driver.find_element(By.XPATH, '//*[@id="loginPassword"]').send_keys(character.password)

    if check_exists_by(By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/p/a', driver):
        driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/p/a').click()

    if threadEvent.is_set():
        return

    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/span').click()

    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/span/div/div[{0}]'.format(character.server)).click()

    if threadEvent.is_set():
        return

    driver.find_element(By.XPATH, '//*[@id="loginButton"]').click()

    if threadEvent.is_set():
        return

    print_with_time(character.user, 'login effettuato')

    time.sleep(30)

    return driver


def missioning(driver, character):
    print_with_time(character.user, '')

    numero_missione = '2' if character.allineamento == 'buono' else '4'

    while not threadEvent.is_set():

        if character.premium:
            if check_exists_by(By.XPATH, '//*[@id="lifeCount"]', driver):
                if driver.find_element(By.XPATH, '//*[@id="lifeCount"]').text == '1':
                    driver.find_element(By.XPATH, '//*[@id="merchPotion335458741"]').click()
                    driver.find_element(By.XPATH, '//*[@id="topPotionPopup"]/div[4]/a[1]/span').click()
                    print_with_time(character.user, 'pozione consumata')

        if check_exists_by(By.XPATH, '//*[@id="navJourney"]', driver):
            driver.find_element(By.XPATH, '//*[@id="navJourney"]').click()
            print_with_time(character.user, 'click su mondo')
            time.sleep(1)
        if check_exists_by(By.XPATH, '//*[@id="' + character.mission_string + '"]', driver):  # default DragonLair
            driver.find_element(By.XPATH, '//*[@id="' + character.mission_string + '"]').click()
            print_with_time(character.user, 'click su missione da svolgere')
            time.sleep(1)
        if check_exists_by(By.XPATH, '//*[@id="sbox-content"]/div/div/p[1]/span', driver):
            if int(driver.find_element(By.XPATH, '//*[@id="sbox-content"]/div/div/p[1]/span').text) < 20:
                # missione con rubino
                driver.find_element(By.XPATH, '//*[@id="sbox-content"]/div/div/div[{}]/ul/li[1]/a[2]'.format(
                    numero_missione)).click()
                print_with_time(character.user, 'click su missione (rubino)')
            else:
                # missione senza rubino
                driver.find_element(By.XPATH, '//*[@id="sbox-content"]/div/div/div[{}]/ul/li[1]/a'.format(
                    numero_missione)).click()
                print_with_time(character.user, 'click su missione (no rubino)')
            time.sleep(1)
            if check_exists_by(By.XPATH, '//*[@id="navJourney"]', driver):
                driver.find_element(By.XPATH, '//*[@id="navJourney"]').click()
                print_with_time(character.user, 'click su mondo')
            time.sleep(360)
        elif check_exists_by(By.XPATH, '//*[@id="progressbarEnds"]', driver):
            t = time.strptime(driver.find_element(By.XPATH, '//*[@id="progressbarEnds"]/span').text, '%H:%M:%S')
            sleep = t.tm_hour * 3600 + (t.tm_min + 1) * 60 + t.tm_sec
            print_with_time(character.user, 'aspetto per {} secondi'.format(sleep))
            time.sleep(sleep)


def thread_start(character):
    d = login(character)
    if threadEvent.is_set():
        return
    missioning(d, character)


def print_with_time(character_name, text):
    t = datetime.datetime.now().time()
    print(t.strftime('[%H:%M:%S]'), '-', character_name, ':', text)


def bk_auto_mission(characters):
    for character in characters:

        if character.enabled is True:
            thread = Thread(target=thread_start, args=(character,))
            threads.append(thread)
            thread.start()
            # thread.join()
