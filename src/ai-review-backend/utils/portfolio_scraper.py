import httpx
from bs4 import BeautifulSoup

def scrape_portfolio(url: str) -> str:
    try:
        response = httpx.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else ''
        headings = " ".join(h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3']))
        paragraphs = " ".join(p.text.strip() for p in soup.find_all('p'))

        content = f"Website Title: {title}\nHeadings: {headings}\nContent: {paragraphs}"
        return content
    except Exception as e:
        return f"Error scraping portfolio: {e}"
