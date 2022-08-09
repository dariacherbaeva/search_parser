import json

from main import LINK, PAGES, JSON_FILENAME
from parser_logic import parse_multiple_pages, save_dict_to_json


def test_json_fields():
    cards_result = parse_multiple_pages(PAGES, LINK)

    assert len(cards_result) == 30

    save_dict_to_json(cards_result, JSON_FILENAME)
    with open(JSON_FILENAME) as file:
        json_data = json.load(file)

    assert json_data
    assert 'Извещение 1' in json_data
    assert 'Номер' in json_data['Извещение 1']
    assert 'Ссылка' in json_data['Извещение 1']
    assert 'Название' in json_data['Извещение 1']
    assert 'Наименование заказчика' in json_data['Извещение 1']
    assert 'ИНН и КПП заказчика' in json_data['Извещение 1']


def test_two_pages():
    assert len(parse_multiple_pages(2, LINK)) == 20


def test_four_pages():
    assert len(parse_multiple_pages(4, LINK)) == 40


def test_one_page():
    assert len(parse_multiple_pages(1, LINK)) == 10
