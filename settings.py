import logging

# Customisable settings
# These should be adjusted to your needs and specifications

# Never give your password online, account id can be email or phone number
ACCOUNT_ID = 'your_facebook_id'
ACCOUNT_PASSWORD = 'your_facebook_password'

# This is a list of ids of all the people you want to send things to
# you can find this id by going to their profile and looking at the url.
PEOPLE_IDS = [
    'user_id_example',
]

# Set this to true if you want to run chromedriver headless
HEADLESS = True


# WARRNING: You should NOT change the following settings

# This must be set to the url of the chromedriver container
CHROMEDRIVER_REMOTE = 'http://chromedriver:4444/wd/hub'

# Messanger settings
_MESSANGER_CONV_URL_PREFIX = 'https://www.facebook.com/messages/t/'
_MESSANGER_URLS = [_MESSANGER_CONV_URL_PREFIX + ID for ID in PEOPLE_IDS]

# Facebook settings
_FACEBOOK_URL = 'http://facebook.com'

# Api settings
_API_URL = 'https://icanhazdadjoke.com/'
_API_HEADERS = {'Accept': 'application/json'}

# Logging settings
LOG_LEVEL = logging.DEBUG
LOG_FILE = 'bot.log'
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {
            'format':
                u"[%(process)d][%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
        }
    },
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard'
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'bot': {
            'handlers': ['file', 'console'],
            'level': LOG_LEVEL
        }
    }
}

