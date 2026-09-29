from fastapi import FastAPI
import re
import datetime
from urllib.parse import urlparse

app = FastAPI()

TRUSTED_DOMAINS = {
    # Fact Checking & Verification
    "snopes.com", "factcheck.org", "politifact.com", "fullfact.org",
    # Global News & Media
    "bbc.com", "bbc.co.uk", "reuters.com", "apnews.com", "aljazeera.com",
    "theguardian.com", "nytimes.com", "washingtonpost.com", "bloomberg.com",
    "npr.org", "dw.com", "france24.com",
    # Knowledge & Reference
    "wikipedia.org", "britannica.com", "archive.org",
    # Academic & Scientific
    "nature.com", "sciencedirect.com", "ncbi.nlm.nih.gov", "arxiv.org", "jstor.org"
}

TRUSTED_TLDS = (".gov", ".edu", ".go.ke")

SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "buff.ly", "ow.ly"}

def extract_urls(text):
    """Extract all HTTP/HTTPS links from raw text using regex."""
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    return re.findall(url_pattern, text)

def clean_domain(url):
    """Extract and normalize domain name from a URL."""
    if not url.startswith(('http://', 'https://.')):
        url = 'http://' + url
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def verify_domain(domain):
    """Determine verification status for a given domain."""
    if domain in SHORTENERS:
        return "SUSPICIOUS (Shortened URL)"
    
    if any(domain.endswith(tld) for tld in TRUSTED_TLDS):
        return "VERIFIED SOURCE (Institutional)"
    
    parts = domain.split('.')
    if len(parts) > 2:
        parent_domain = '.'.join(parts[-2:])
        if parent_domain in TRUSTED_DOMAINS:
            return "VERIFIED SOURCE"
            
    if domain in TRUSTED_DOMAINS:
        return "VERIFIED SOURCE"
        
    return "UNVERIFIED SOURCE"

@app.get("/")
def read_root():
    return {"message": "SourcedIt API is live and operational!"}

@app.get("/scan")
def scan_text(text: str):
    urls = extract_urls(text)
    if not urls:
        return {"message": "No valid URLs detected in the provided text.", "results": []}
    
    scan_results = []
    for url in urls:
        domain = clean_domain(url)
        status = verify_domain(domain)
        scan_results.append({"url": url, "domain": domain, "status": status})
        
    return {"total_found": len(urls), "results": scan_results}
