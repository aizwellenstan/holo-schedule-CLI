#Scrape today's schedule from Hololive official schedule

import os
import sys

from src.util import *

import requests


def remove_text(text, date):

    text_list = text.split('\n')

    #Delete null element and escape charactors and space in text_list
    text_list = tuple(map(lambda s: s.replace(' ', ''), text_list))
    text_list = tuple(map(lambda s: s.replace('\r', ''), text_list))
    text_list = tuple(map(lambda s: s.replace(' ', ''), text_list))

    try:
        date_index = text_list.index(date)
    
    #Sometimes there is no streming at tomorrow's schedule
    except:
        print('No streming found on tomorrow')
        sys.exit()


    text_list = text_list[date_index:]

    SPAN = '<divclass="holodulenavbar-text"style="letter-spacing:0.3em;">'

    try:
        last_index = text_list.index(SPAN)

    except ValueError:
        last_index = -10

    text_list = text_list[0:last_index]

    return text_list
 

#Fetch all stream in the day
def fetch_source_html(date):

    SOURCE_URL = 'https://schedule.hololive.tv/simple'
    #Temporary user agent
    HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

    try:
        req = requests.get(SOURCE_URL, headers=HEADER, timeout=3)

    except Exception:
        print("Connection timeout")
        sys.exit()

    if req.status_code != 200:
        print("An error occured!")
        sys.exit()

    text_list = remove_text(req.text, date)

    return text_list
