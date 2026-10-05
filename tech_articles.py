import re
import time
from urllib.parse import urljoin, urlparse, quote

import requests
from bs4 import BeautifulSoup
import trafilatura


MAGAZINES = {
    "CNET": "https://www.cnet.com/",
    "ZDNET": "https://www.zdnet.com/",
    "PCMag": "https://www.pcmag.com/",
    "PCWorld": "https://www.pcworld.com/",
    "TechRadar": "https://www.techradar.com/",
    "Tom's Guide": "https://www.tomsguide.com/",
    "Tom's Hardware": "https://www.tomshardware.com/",
}


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    )
}


def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_valid_article_url(url, domain):
    if not url:
        return False

    parsed = urlparse(url)

    if domain not in parsed.netloc:
        return False

    ignored = [
        "/video/",
        "/podcasts/",
        "/newsletters/",
        "/search/",
        "/author/",
        "/category/",
        "/tag/",
        "/gallery/",
    ]

    return not any(x in parsed.path.lower() for x in ignored)


def extract_article(url, magazine):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        if response.status_code != 200:
            return None

        downloaded = trafilatura.fetch_url(url)

        if not downloaded:
            downloaded = response.text

        article_text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            favor_precision=True
        )

        if not article_text:
            soup = BeautifulSoup(response.text, "html.parser")

            paragraphs = soup.find_all("p")

            article_text = " ".join(
                p.get_text(" ", strip=True)
                for p in paragraphs
            )

        article_text = clean_text(article_text)

        if len(article_text) < 300:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        title = ""

        if soup.title:
            title = soup.title.get_text(" ", strip=True)

        if not title:
            h1 = soup.find("h1")
            if h1:
                title = h1.get_text(" ", strip=True)

        return {
            "source": magazine,
            "title": clean_text(title),
            "url": url,
            "text": article_text,
        }

    except Exception:
        return None


def discover_links(search_url, magazine, domain, max_results=5):
    try:
        response = requests.get(
            search_url,
            headers=HEADERS,
            timeout=20
        )

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        links = []

        for a in soup.find_all("a", href=True):
            href = a.get("href")

            if href.startswith("/"):
                href = urljoin(search_url, href)

            if not href.startswith("http"):
                continue

            if not is_valid_article_url(href, domain):
                continue

            if href not in links:
                links.append(href)

            if len(links) >= max_results:
                break

        return links

    except Exception:
        return []


def search_magazine(magazine, base_url, query, max_articles=3):
    domain = urlparse(base_url).netloc

    encoded_query = quote(query)

    # Publication-specific search pages
    search_urls = {
        "CNET": f"{base_url}search/?query={encoded_query}",
        "ZDNET": f"{base_url}search/?q={encoded_query}",
        "PCMag": f"{base_url}search/?q={encoded_query}",
        "PCWorld": f"{base_url}search/?q={encoded_query}",
        "TechRadar": f"{base_url}search?searchTerm={encoded_query}",
        "Tom's Guide": f"{base_url}search?searchTerm={encoded_query}",
        "Tom's Hardware": f"{base_url}search?searchTerm={encoded_query}",
    }

    search_url = search_urls.get(magazine)

    if not search_url:
        return []

    links = discover_links(
        search_url,
        magazine,
        domain,
        max_results=max_articles * 3
    )

    articles = []

    for url in links:

        article = extract_article(url, magazine)

        if article:
            articles.append(article)

        if len(articles) >= max_articles:
            break

        time.sleep(0.5)

    return articles


def search_all_magazines(query, max_articles_per_source=3):
    all_articles = []

    for magazine, base_url in MAGAZINES.items():

        articles = search_magazine(
            magazine,
            base_url,
            query,
            max_articles=max_articles_per_source
        )

        all_articles.extend(articles)

    return all_articles


def create_article_dataframe(articles):
    import pandas as pd

    if not articles:
        return pd.DataFrame(
            columns=[
                "source",
                "title",
                "url",
                "text"
            ]
        )

    df = pd.DataFrame(articles)

    df = df.drop_duplicates(
        subset=["url"]
    ).reset_index(drop=True)

    return df