# SourcedIt

**SourcedIt** is a lightweight Python utility designed to scan text or Reddit posts, extract embedded links, and verify them against a list of trusted media and organizational sources.

---

## Features

- **Link Extraction:** Automatically parses input text to detect standard HTTP and HTTPS web links.
- **Source Verification:** Cross-references extracted links against an internal list of approved domains.
- **Status Reporting:** Provides immediate feedback in the console:
  - `VERIFIED SOURCE` for trusted domains.
  - `UNVERIFIED SOURCE` for unlisted domains.
- **Interactive CLI:** Runs continuously in the terminal until explicitly exited.

---

## How It Works

1. Run the `main.py` script in your terminal.
2. Paste any raw text or Reddit post content containing URLs.
3. The engine extracts the URLs and returns a verification report for each link detected.

---

## Usage

### Prerequisites
- Python 3.x installed on your machine.

### Running the Script

1. Clone or download this repository.
2. Open a terminal in the project directory and run:

```bash
python main.py
