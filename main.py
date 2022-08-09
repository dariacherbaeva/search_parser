from parser_logic import save_dict_to_json, parse_multiple_pages

LINK = 'https://www.rts-tender.ru/poisk'
PAGES = 3
JSON_FILENAME = 'result_data.json'

cards_result = parse_multiple_pages(PAGES, LINK)

save_dict_to_json(cards_result, JSON_FILENAME)
