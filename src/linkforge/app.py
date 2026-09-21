import string
import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

app = FastAPI()

# In-memory store (use a database in production)
url_store: dict[str, str] = {}


def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


@app.post("/shorten")
def shorten_url(url: str) -> dict:
    """Accept a long URL as a query parameter and return a short code."""
    short_code = generate_short_code()
    while short_code in url_store:
        print(f"Collision detected for short code: {short_code}. Generating a new one.")
        short_code = generate_short_code()  # Ensure uniqueness
    url_store[short_code] = url
    return {"short_code": short_code, "short_url": f"http://127.0.0.1:8000/{short_code}"}


@app.get("/{short_code}")
def redirect_url(short_code: str):
    original_url = url_store.get(short_code)

    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url=original_url)