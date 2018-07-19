import time
import logging
from multiprocessing import Pool
from logging.config import dictConfig

import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import settings


dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger('bot')


def get_configured_driver():
    """Start and configure a selenium webdriver.

    The configs can be adjusted in setting.py file
    and are documented there.
    """
    options = webdriver.ChromeOptions()

    # Notifications and pop-ups are disabled by default
    options.add_argument('--disable-notifications')

    if settings.HEADLESS:
        options.add_argument('--headless')

    driver = webdriver.Remote(
        settings.CHROMEDRIVER_REMOTE, options.to_capabilities())

    return driver


def setup_facebook_login_in_session(driver):
    """Login to facebook to get session cookies."""
    driver.get(settings._FACEBOOK_URL)

    email_input = driver.find_element_by_xpath(
        '//input[@data-testid="royal_email"]')
    email_input.send_keys(settings.ACCOUNT_ID)

    password_input = driver.find_element_by_xpath(
        '//input[@data-testid="royal_pass"]')
    password_input.send_keys(settings.ACCOUNT_PASSWORD)

    login_button = driver.find_element_by_xpath(
        '//input[@data-testid="royal_login_button"]')
    login_button.click()


def send_text_in_messanger(driver, text):
    """Send text in messanger."""
    ActionChains(driver).send_keys(text).key_up(Keys.ENTER).perform()


def get_new_joke():
    """Call jokes api for a new random joke.

    The api used here is offered for free by icanhazdadjoke.
    For more info about the api go to https://icanhazdadjoke.com/api
    """
    return requests.get(
        settings._API_URL, headers=settings._API_HEADERS).json()['joke']


def start_trollbot(facebook_user_conv_url):
    logger.info('Starting trollbot version 3.0 for {}!'.format(
        facebook_user_conv_url.split('/')[-1]))

    logger.info('Setting up driver...')
    driver = get_configured_driver()
    logger.info('Driver setup succesful!')

    logger.info('Logging in to facebook...')
    setup_facebook_login_in_session(driver)
    logger.info('Login succesful!')

    driver.get(facebook_user_conv_url)

    while True:
        time.sleep(1)

        joke = get_new_joke()
        logger.info('About to tell this joke\t{}'.format(joke))

        send_text_in_messanger(driver, joke)
        logger.info('Joke was succesfully sent!')

    driver.close()


if __name__ == '__main__':
    pool = Pool(len(settings._MESSANGER_URLS))
    pool.map(start_trollbot, settings._MESSANGER_URLS)
