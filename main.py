import re
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="SourcedIt API", version="1.1.0")

# Authorized keys dictionary
VALID_API_KEYS = {"sarafina_secret_key_123"}


class URLRequest(BaseModel):
  text: str


@app.get("/")
def read_root():
  return {
      "status": "online",
      "message": "Welcome to SourcedIt API! Endpoint /verify is protected.",
  }


@app.post("/verify")
def verify_urls(
    payload: URLRequest,
    x_api_key: str = Header(
        None, description="Enter your API key here (e.g., sarafina_secret_key_123)"
    ),
):
  # 1. Security Check
  if not x_api_key or x_api_key not in VALID_API_KEYS:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key. Please provide a valid x-api-key.",
    )

  # 2. Advanced Extraction & Verification Logic
  url_pattern = r"https?://[^\s]+"
  raw_urls = re.findall(url_pattern, payload.text)

  cleaned_urls = []
  secure_count = 0
  insecure_count = 0
  domains = set()

  for url in raw_urls:
    clean_url = url.rstrip(".,;:?!')\"]")
    if clean_url not in cleaned_urls:
      cleaned_urls.append(clean_url)

      # Track secure (https) vs insecure (http) links
      if clean_url.startswith("https://"):
        secure_count += 1
      else:
        insecure_count += 1

      # Extract the root domain (e.g., github.com from https://github.com/sarafina)
      domain_match = re.search(r"https?://([^/]+)", clean_url)
      if domain_match:
        domains.add(domain_match.group(1))

  # 3. Clean, Professional Response Layout
  return {
      "status": "success",
      "auth": "verified",
      "summary": {
          "total_urls_found": len(cleaned_urls),
          "secure_links": secure_count,
          "insecure_links": insecure_count,
          "unique_domains": list(domains),
      },
      "extracted_urls": cleaned_urls,
      "message": (
          f"Successfully analyzed text and found {len(cleaned_urls)} unique"
          " URL(s)."
      ),
  }
