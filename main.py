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
  # Put your URL extraction and domain verification logic here
  # For example, returning the received text or verification results:
  return {
      "status": "success",
      "received_text": payload.text,
      "message": "Verification logic ready to execute!",
  }
