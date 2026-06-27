import os
import requests
from bs4 import BeautifulSoup

BASE_DIR = "faculties"
os.makedirs(BASE_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}


# universitetlar
with open("universities.txt", "r", encoding="utf-8") as f:
    for uni_id, line in enumerate(f, start=1):

        parts = line.strip().split("|")
        if len(parts) < 2:
            continue

        name, url = parts[0], parts[1]

        try:
            res = requests.get(url, headers=headers, timeout=30)
            res.raise_for_status()

            soup = BeautifulSoup(res.text, "html.parser")

            section = soup.find("section", id="directions")
            if not section:
                print("No section:", uni_id)
                continue

            divs = section.find_all("div", recursive=False)
            if len(divs) < 2:
                print("No container:", uni_id)
                continue

            container = divs[1]
            articles = container.find_all("article")

            file_path = f"{BASE_DIR}/{uni_id}.txt"

            with open(file_path, "w", encoding="utf-8") as out:

                for article in articles:

                    h3 = article.find("h3")
                    fname = h3.get_text(strip=True) if h3 else ""

                    try:
                        base = article.find_all("div")[0].find_all("div")[1]

                        language = base.find_all("div")[0].find_all("span")[0].get_text(strip=True)
                        type_ = base.find_all("div")[1].find_all("span")[0].get_text(strip=True)
                        price = base.find_all("div")[2].find_all("span")[0].get_text(strip=True)

                    except:
                        language = ""
                        type_ = ""
                        price = ""

                    out.write(f"{fname}|{language}|{type_}|{price}\n")

            print("Yozildi:", file_path)

        except Exception as e:
            print("Xato:", uni_id, e)