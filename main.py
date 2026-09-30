import re
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class URLRequest(BaseModel):
  text: str


@app.get("/")
def read_root():
  return {"message": "SourcedIt API is live and operational!"}


@app.post("/verify")
def verify_urls(payload: URLRequest):
  # Standard regex to find http/https URLs
  url_pattern = r"https?://[^\s]+"
  raw_urls = re.findall(url_pattern, payload.text)

  # Clean trailing punctuation and remove duplicates while preserving order
  cleaned_urls = []
  for url in raw_urls:
    # Strip common punctuation that might accidentally cling to the end of a URL
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
