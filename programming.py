from os import path
import urllib.request as urllib
import xml.etree.ElementTree as ET
from datetime import datetime
import telegram

CHANNELS_TO_SCAN = [
    'BandSports', 
    'ESPN', 
    'ESPN 2', 
    'ESPN Brasil', 
    'ESPN Extra', 
    'Esporte Interativo', 
    'FOX Premium 1', 
    'FOX Premium 2', 
    'FOX Sports', 
    'FOX Sports 2', 
    'Premiere Clubes', 
    'Premiere 2', 
    'Premiere 3', 
    'Premiere 4', 
    'Premiere 5', 
    'Premiere 6', 
    'Premiere 7', 
    'Premiere 8 - Mosaico', 
    'Premiere 9', 
    'SporTV', 
    'SporTV 2', 
    'SporTV 3'
]

PROGRAMMES_TO_EXCLUDE = [
    'Sportscenter', 
    'Bate-Bola Debate', 
    'Futebol no Mundo', 
    'Futebol na Veia', 
    'Pré Jogo', 
    'Fox Sports Rádio', 
    'Expediente Futebol', 
    'Debate Final', 
    'Tá na Área', 
    'Troca de Passes', 
    'A Última Palavra'
]

KEYWORDS = [
    'Vivo', 
    'Laliga'
]

def title_has_any_keyword(title): 
    if PROGRAMMES_TO_EXCLUDE: 
        for programme in PROGRAMMES_TO_EXCLUDE: 
            if programme in title: 
                return False
    if KEYWORDS: 
        for keyword in KEYWORDS: 
            if keyword in title: 
                return True
        return False
    else: 
        return True

today = datetime.today().strftime('%Y-%m-%d')
today_filename = 'epg/epg-{}.xml'.format(today)

if path.exists(today_filename): 
    print('epg file already downloaded')
else: 
    print('start downloading epg file...')
    urllib.urlretrieve('http://tvepg.co', today_filename)
    print('finished downloading epg file')

root = ET.parse(today_filename).getroot()

print('channels to scan: {}'.format(CHANNELS_TO_SCAN))

channels = {}

for channel in CHANNELS_TO_SCAN: 
    
    node = root.find("channel/[display-name='{}']".format(channel))
    
    if node: 
        channels[channel] = {
            'id': node.get('id')
        }
    else: 
        print("'{}' not found".format(channel))

print('channels found: {}'.format(channels))

for channel, data in channels.items(): 

    channel_id = data['id']
    programmes = root.findall("programme[@channel='{}']".format(channel_id))

    print('{} programming results for {}'.format(len(programmes), channel))

    programmes_selected = []

    for programme in programmes: 

        title = programme.find('title').text

        start = programme.get('start')
        start = datetime.strptime(start, '%Y%m%d%H%M%S %z')

        if title_has_any_keyword(title) and start.date() == datetime.today().date(): 
            programmes_selected.append('{} - {}'.format(start.strftime('%H:%M'), title))
    
    print('{} programmes selected to notify for {}'.format(len(programmes_selected), channel))
    
    if programmes_selected: 
        message = telegram.make_message(channel, programmes_selected)
        telegram.send_message(message)
