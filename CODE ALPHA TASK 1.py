import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

books = []

for page in range(1, 6):  # scrape first 5 pages
    url = BASE_URL.format(page)
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for item in soup.select("article.product_pod"):
        title = item.h3.a.get("title", "").strip()
        price = item.select_one(".price_color").get_text(strip=True)
        availability = item.select_one(".availability").get_text(" ", strip=True)
        rating = item.p.get("class", ["", ""])[1]

        rating_map = {
            "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
        }

        books.append({
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating_map.get(rating, None),
            "page": page
        })

    time.sleep(0.5)

df = pd.DataFrame(books)
df["price_gbp"] = (
    df["price"].str.replace(r"[^\d.]", "", regex=True).astype(float)
)

df.to_csv("books_scraped.csv", index=False, encoding="utf-8-sig")

print(f"Scraped {len(df)} books.")
print(df.head())
