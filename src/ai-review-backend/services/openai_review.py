import openai
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import httpx
from bs4 import BeautifulSoup

load_dotenv()
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def fetch_website_text(url: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator=' ', strip=True)
            return text[:5000]  # Trim long pages
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

async def generate_review(url: str) -> str:
    content = ""

    try:
        if "github.com" in url:
            content = await fetch_github_readme(url)
        else:
            content = await fetch_website_text(url)

        prompt = f"""
        You are a professional web and AI portfolio reviewer.
        Here's the portfolio content:

        \"\"\"{content}\"\"\"

        Give a friendly, detailed critique with suggestions to improve.
        """

        response = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI API error: {e}"