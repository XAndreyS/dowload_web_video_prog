import json

parser = {
    1: 'bs4',
    2: 'selenium'
}

with open('set_parser.json', 'w', encoding='utf8') as file:
            json.dump(parser, file, ensure_ascii=False, indent=4)