import re
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="SourcedIt API", version="1.2.0")

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
  if not x_api_key or x_api_key not in VALID_API_KEYS:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key. Please provide a valid x-api-key.",
    )

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

      if clean_url.startswith("https://"):
        secure_count += 1
      else:
        insecure_count += 1

      domain_match = re.search(r"https?://([^/]+)", clean_url)
      if domain_match:
        domains.add(domain_match.group(1))

  # Cleaner, reorganized response structure
  return {
      "success": True,
      "message": (
          f"Successfully processed text and extracted {len(cleaned_urls)}"
          " unique URL(s)."
      ),
      "analytics": {
          "total_urls": len(cleaned_urls),
          "secure_https": secure_count,
          "insecure_http": insecure_count,
          "unique_domains": sorted(list(domains)),
      },
      "data": {"urls": cleaned_urls},
  }
