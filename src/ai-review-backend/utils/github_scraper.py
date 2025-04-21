import httpx
import base64

def scrape_github_repo(url: str) -> str:
    try:
        if "github.com" not in url:
            return ""

        parts = url.strip("/").split("/")
        username, repo = parts[-2], parts[-1]

        api_url = f"https://api.github.com/repos/{username}/{repo}/readme"
        res = httpx.get(api_url, headers={"Accept": "application/vnd.github.v3+json"})

        if res.status_code == 200:
            content = res.json().get("content", "")
            decoded = base64.b64decode(content).decode("utf-8")
            return f"README:\n{decoded}"
        else:
            return "Could not fetch README."

    except Exception as e:
        return f"Error scraping GitHub: {e}"
