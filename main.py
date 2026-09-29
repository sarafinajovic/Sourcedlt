import re
import datetime
from urllib.parse import urlparse

# Base set of verified domains (news, reference, government, academic, fact-checkers)
TRUSTED_DOMAINS = {
    # Fact Checking & Verification
    "snopes.com", "factcheck.org", "politifact.com", "fullfact.org",
    
    # Global News & Media
    "bbc.com", "bbc.co.uk", "reuters.com", "apnews.com", "aljazeera.com",
    "theguardian.com", "nytimes.com", "washingtonpost.com", "bloomberg.com",
    "npr.org", "dw.com", "france24.com",
    
    # Knowledge & Reference
    "wikipedia.org", "britannica.com", "archive.org",
    
    # Academic & Research
    "nature.com", "sciencedirect.com", "ncbi.nlm.nih.gov", "arxiv.org", "jstor.org"
}

# Common TLDs automatically trusted for official institutions
TRUSTED_TLDS = (".gov", ".edu", ".go.ke")

# URL shorteners that mask the true source
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "buff.ly", "ow.ly"}


def extract_urls(text):
    """Extract all HTTP/HTTPS links from raw text using regex."""
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    return re.findall(url_pattern, text)


def clean_domain(url):
    """Extract and normalize domain name from a URL."""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    # Strip 'www.' if present
    if domain.startswith('www.'):
        domain = domain[4:]
        
    return domain


def verify_domain(domain):
    """Determine verification status for a given domain."""
    if domain in SHORTENERS:
        return "SUSPICIOUS (Shortened URL)"
    
    # Check trusted TLD suffixes (.gov, .edu, etc.)
    if any(domain.endswith(tld) for tld in TRUSTED_TLDS):
        return "VERIFIED SOURCE (Institutional)"
        
    # Check explicit domain list and main parent domains
    parts = domain.split('.')
    if len(parts) > 2:
        parent_domain = '.'.join(parts[-2:])
        if parent_domain in TRUSTED_DOMAINS:
            return "VERIFIED SOURCE"
            
    if domain in TRUSTED_DOMAINS:
        return "VERIFIED SOURCE"
        
    return "UNVERIFIED SOURCE"


def log_results(text_input, results):
    """Append verification session details to a local log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    snippet = text_input[:50].replace('\n', ' ') + "..." if len(text_input) > 50 else text_input.replace('\n', ' ')
    
    with open("sourcedit_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"\n--- Scan Session: {timestamp} ---\n")
        log_file.write(f"Input Snippet: \"{snippet}\"\n")
        log_file.write("Results:\n")
        for url, status, domain in results:
            log_file.write(f"  - [{status}] {url} ({domain})\n")


def main():
    print("=" * 55)
    print("           SourcedIt Engine v1.1 - Live Scan           ")
    print("=" * 55)
    print("Paste text containing links to verify sources.")
    print("Type 'exit' or 'quit' to terminate the engine.\n")

    while True:
        try:
            user_input = input("SourcedIt > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting SourcedIt. Goodbye!")
            break

        if user_input.lower() in ['exit', 'quit']:
            print("Exiting SourcedIt. Goodbye!")
            break

        if not user_input:
            continue

        urls = extract_urls(user_input)

        if not urls:
            print("  [!] No valid URLs detected in the provided text.\n")
            continue

        print(f"\nFound {len(urls)} link(s) to analyze:")
        scan_results = []
        
        for url in urls:
            domain = clean_domain(url)
            status = verify_domain(domain)
            scan_results.append((url, status, domain))
            
            # Console Output Formatting
            flag = "[✓]" if "VERIFIED" in status else "[?]" if "UNVERIFIED" in status else "[!]"
            print(f"  {flag} {status}: {url}")
            print(f"      Domain: {domain}")

        # Automatically record to local history
        log_results(user_input, scan_results)
        print("\n[Log updated in 'sourcedit_log.txt']\n" + "-" * 55 + "\n")


if __name__ == "__main__":
    main()