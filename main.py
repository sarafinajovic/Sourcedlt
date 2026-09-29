import re
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class URLRequest(BaseModel):
  text: str


@app.get("/")
def read_root():
  return {"message": "SourcedIt is live!"}


@app.post("/verify")
def verify_urls(payload: URLRequest):
  # Regular expression to find http/https URLs in the text
  url_pattern = r"https?://[^\s]+"
  found_urls = re.findall(url_pattern, payload.text)

  return {
      "status": "success",
      "received_text": payload.text,
      "extracted_urls": found_urls,
      "url_count": len(found_urls),
      "message": f"Successfully scanned text and found {len(found_urls)} URL(s).",
  }
