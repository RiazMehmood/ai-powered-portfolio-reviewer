import google.generativeai as genai
import os
from dotenv import load_dotenv
import httpx
from bs4 import BeautifulSoup

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def fetch_website_text(url: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator=' ', strip=True)
            return text[:5000]
    except Exception as e:
        return f"Failed to fetch site: {e}"

async def fetch_github_readme(url: str) -> str:
    try:
        parts = url.strip("/").split("/")
        username, repo = parts[-2], parts[-1]
        raw_url = f"https://raw.githubusercontent.com/{username}/{repo}/main/README.md"
        async with httpx.AsyncClient() as client:
            response = await client.get(raw_url, timeout=10)
            return response.text[:5000]
    except Exception as e:
        return f"Failed to fetch GitHub README: {e}"

async def generate_review_gemini(url: str) -> str:
    try:
        if "github.com" in url:
            content = await fetch_github_readme(url)
        else:
            content = await fetch_website_text(url)

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(
            f"""
            You are a professional portfolio reviewer. Here's the portfolio content:

            \"\"\"{content}\"\"\"

            Provide a helpful, friendly review with suggestions to improve it.
            """
        )
        return response.text
    except Exception as e:
        return f"Gemini API error: {e}"
