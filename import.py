import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://mentalaba.uz"

headers = {
    "User-Agent": "Mozilla/5.0"
}

with open("universities.txt", "w", encoding="utf-8") as f:

    for page in range(1, 9):  # 1-8 sahifalar

        url = f"https://mentalaba.uz/universities?page={page}"
        print(f"Yuklanmoqda: {url}")

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for article in soup.find_all("article"):

            # Universitet nomi
            h3 = article.find("h3")
            title = h3.get_text(strip=True) if h3 else ""

            # Rasm URL
            img = article.find("img")
            img_url = ""
            if img:
                img_url = urljoin(BASE_URL, img.get("src", ""))

            # Universitet sahifasi URL
            a = article.find_parent("a")
            href = ""
            if a:
                href = urljoin(BASE_URL, a.get("href", ""))

            f.write(f"{title}|{href}|{img_url}\n")

print("Barcha 8 ta sahifa saqlandi.")