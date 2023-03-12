from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from collections import defaultdict
import argparse
import os
from dotenv import load_dotenv


def correct_year_name(delta):
    if int(delta[-2:]) in range(11, 21):
        return "лет"
    elif delta[-1] == "1":
        return "год"
    elif int(delta[-1]) in range(2, 5):
        return "года"
    else:
        return "лет"


def wines(winefile_path):
    wines = pandas.read_excel(winefile_path, na_values=' ', keep_default_na=False). \
        to_dict(orient='records')

    all_wines = defaultdict(list)
    for wine in wines:
        all_wines[wine['Категория']].append(wine)

    return all_wines


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Путь к файлу, содержащему базу данных для сайта")
    parser.add_argument('--path', help='Путь к файлу',
                        default=os.getenv('WINES_FILE_PATH', default='wines_table.xlsx'))
    args = parser.parse_args()
    winefile_path = args.path

    foundation_year = 1920

    years_passed = str(datetime.datetime.now().year - foundation_year)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        years=years_passed,
        years_name=correct_year_name(years_passed),
        wines_types=wines(winefile_path),
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
