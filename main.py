import re

# List of trusted and verified domains
TRUSTED_DOMAINS = [
    "wikipedia.org", 
    "reuters.com", 
    "apnews.com", 
    "nature.com", 
    "arxiv.org"
]

def verify_submission_sources(text_content):
    print("\nScanning text for links...")
    found_urls = re.findall(r'(https?://[^\s]+)', text_content)

    if not found_urls:
        print("No URLs found in the text.\n")
        return

    for url in found_urls:
        print(f"Checking link: {url}")
        is_trusted = any(domain in url.lower() for domain in TRUSTED_DOMAINS)

        if is_trusted:
            print("Status: VERIFIED SOURCE (Trusted domain matched)\n")
        else:
            print("Status: UNVERIFIED SOURCE (Not on the approved list)\n")

# Loop so you can test multiple times
while True:
    user_text = input("Paste a Reddit post or text to check (or type 'exit' to quit): ")
    if user_text.lower() == 'exit':
        print("Exiting SourcedIt. Goodbye!")
        break
    verify_submission_sources(user_text)