import time
import logging
from logging.config import dictConfig

import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from settings import (
    HEADLESS, CHROMEDRIVER_PATH, _FACEBOOK_URL,
    ACCOUNT_ID, ACCOUNT_PASSWORD, _API_HEADERS,
    _API_URL, _MESSANGER_URLS, LOGGING_CONFIG
)


dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('bot')


def get_configured_driver():
    """Start and configure a selenium webdriver.

    The configs can be adjusted in setting.py file
    and are documented there.
    """
    options = webdriver.ChromeOptions()

    # Notifications and pop-ups are disabled by default
    options.add_argument('--disable-notifications')

    if HEADLESS:
        options.add_argument('--headless')

    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

    return driver


def setup_facebook_login_in_session(driver):
    """Login to facebook to get session cookies."""
    driver.get(_FACEBOOK_URL)

    email_input = driver.find_element_by_xpath(
        '//input[@data-testid="royal_email"]')
    email_input.send_keys(ACCOUNT_ID)

    password_input = driver.find_element_by_xpath(
        '//input[@data-testid="royal_pass"]')
    password_input.send_keys(ACCOUNT_PASSWORD)

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
    return requests.get(_API_URL, headers=_API_HEADERS).json()['joke']


if __name__ == '__main__':
    logger.info('Starting trollbot version 3.0!')

    logger.info('Setting up driver...')
    driver = get_configured_driver()
    logger.info('Driver setup succesful!')

    logger.info('Logging in to facebook...')
    setup_facebook_login_in_session(driver)
    logger.info('Login succesful!')

    logger.info('Starting the trolling...')
    while True:
        time.sleep(1)
        joke = get_new_joke()

        logger.info(
            'About to tell everybody this joke\n\t{}'.format(joke))

        for url in _MESSANGER_URLS:
            logger.info(
                'Going to messanger url {} to tell the joke...'.format(url))

            # This is a sanity check in case to cut requests
            # when there's only one url
            if driver.current_url != url:
                driver.get(url)
            logger.info(
                'Get request was succesfull,'
                'now driver should be on page {}!'.format(url)
            )

            # Safety check for messanger page fully loading
            time.sleep(1)

            logger.info('Send the joke...')
            send_text_in_messanger(driver, joke)

            # This is required so that we don't get the
            # 'are you sure you want to leave' pop-up
            time.sleep(3)

            logger.info('Joke was succesfully sent!')

    driver.close()
