import logging as log
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
TELEGRAM_PARSE_MODE = os.environ.get('TELEGRAM_PARSE_MODE')

def send_message(message): 
    url = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/sendMessage?chat_id=' + TELEGRAM_CHAT_ID + '&parse_mode=' + TELEGRAM_PARSE_MODE + '&text=' + message
    log.info('request to <{}>'.format(url))
    requests.get(url)

def send_photo(photo, caption): 
    url = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/sendPhoto?chat_id=' + TELEGRAM_CHAT_ID + '&photo=' + photo + '&parse_mode=' + TELEGRAM_PARSE_MODE + '&caption=' + caption
    log.info('request to <{}>'.format(url))
    requests.get(url)

def make_message(channel, programmes): 
    message = '*{}*'.format(channel)
    for programme in programmes: message += '\n{}'.format(programme)
    return message
