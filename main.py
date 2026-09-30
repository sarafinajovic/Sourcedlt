import re
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="SourcedIt API", version="1.0.0")

# Authorized keys dictionary
VALID_API_KEYS = {"sarafina_secret_key_123"}


class URLRequest(BaseModel):
  text: str


@app.get("/")
def read_root():
  return {
      "message": "Welcome to SourcedIt API! Endpoint /verify is protected."
  }


@app.post("/verify")
def verify_urls(
    payload: URLRequest,
    x_api_key: str = Header(
        None, description="Enter your API key here (e.g., sarafina_secret_key_123)"
    ),
):
  # Check if the provided key is valid
  if not x_api_key or x_api_key not in VALID_API_KEYS:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key. Please provide a valid x-api-key.",
    )

  # Standard regex to find http/https URLs
  url_pattern = r"https?://[^\s]+"
  raw_urls = re.findall(url_pattern, payload.text)

  # Clean trailing punctuation and remove duplicates while preserving order
  cleaned_urls = []
  for url in raw_urls:
    clean_url = url.rstrip(".,;:?!')\"]")
    if clean_url not in cleaned_urls:
      cleaned_urls.append(clean_url)

  return {
      "status": "success",
      "received_text": payload.text,
      "extracted_urls": cleaned_urls,
      "url_count": len(cleaned_urls),
      "message": f"Successfully extracted {len(cleaned_urls)} unique URL(s).",
  }
