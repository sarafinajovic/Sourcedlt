import re
from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

app = FastAPI(title="SourcedIt API", version="1.0.0")

# Define the header name clients must include
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Authorized keys dictionary (we can later connect this to a database)
# For now, your personal admin key is included here:
VALID_API_KEYS = {"sarafina_secret_key_123"}


def get_api_key(api_key: str = Security(api_key_header)):
  if not api_key or api_key not in VALID_API_KEYS:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key. Please provide a valid x-api-key header.",
    )
  return api_key


class URLRequest(BaseModel):
  text: str


@app.get("/")
def read_root():
  return {
      "message": "Welcome to SourcedIt API! Endpoint /verify is protected."
  }


@app.post("/verify")
def verify_urls(payload: URLRequest, api_key: str = Security(get_api_key)):
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
