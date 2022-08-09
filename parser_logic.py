import json
import re

import requests
from bs4 import BeautifulSoup

PARSE_TEXT = 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36'


def parse_page(link: str):
    response = requests.get(link, headers={'User-Agent': PARSE_TEXT})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def find_cards(soup):
    return soup.findAll('div', {'class': 'cards'})


def get_card_info(card):
    card_info = dict()
    item_about = card.find('div', {'class': 'card-item__about'})
    number = item_about.text.strip()
    card_info['Номер'] = number
    link = item_about.find('a', {'class': 'link'})['href']
    card_info['Ссылка'] = link
    title = card.find('div', {'class': 'card-item__title'}).text.strip()
    card_info['Название'] = title
    organization = card.findAll('div', {'class': 'card-item__organization-main'})[1]
    organization_ps = organization.findAll('p')
    organization_title = organization_ps[0].find('span').text.strip()
    card_info['Наименование заказчика'] = organization_title
    organization_info = organization_ps[1].text.strip()
    organization_inn_kpp = re.findall('(.*).', organization_info)[0]
    card_info['ИНН и КПП заказчика'] = organization_inn_kpp
    return card_info


def parse_multiple_pages(pages, parse_link):
    counter = 1
    cards_result = dict()
    for i in range(1, pages + 1):
        link = f'{parse_link}?page={i}'
        soup = parse_page(link)

        cards = find_cards(soup)

        for card in cards:
            card_info = get_card_info(card)
            cards_result[f'Извещение {counter}'] = card_info
            counter += 1
    return cards_result


def save_dict_to_json(cards_dict, filename):
    result_json = json.dumps(cards_dict, indent=4, ensure_ascii=False)

    with open(filename, 'w') as file:
        file.write(result_json)
