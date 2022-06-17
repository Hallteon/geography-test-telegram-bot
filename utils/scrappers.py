import requests
from bs4 import BeautifulSoup

from data.config import USER_AGENT

headers = {"accept": "*/*",
           "user-agent": USER_AGENT}


async def countries_scrapper():
    data = {}

    url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D1%82%D0%BE%D0%BB%D0%B8%D1%86_" \
          "%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2 "

    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")

    main_block = soup.find("div", class_="mw-parser-output")
    titles = main_block.find_all("h2")[1:]
    tables = main_block.find_all("table", class_="wikitable")

    for title, table in zip(titles, tables):
        names = {}
        table_body = table.find("tbody")
        counties_data = table_body.find_all("tr")[1:]

        for countrie in counties_data:
            try:
                content = countrie.find_all("td")

                name = content[1].find("span", class_="wrap")
                capital = content[2].find("a")

                names[name.text.strip()] = capital.text.strip()
            except:
                continue

        data[title.text.strip()] = names

    print(data)

