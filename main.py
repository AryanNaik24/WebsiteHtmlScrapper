import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def download_file(session, url, folder):
    """Download a single file into the given folder."""
    local_filename = os.path.join(folder, os.path.basename(urlparse(url).path))
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        with open(local_filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {url} -> {local_filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def scrape_website(base_url, output_folder="website_data"):
    os.makedirs(output_folder, exist_ok=True)
    session = requests.Session()

    # Get main HTML
    response = session.get(base_url, timeout=10)
    response.raise_for_status()
    html_content = response.text

    # Save main HTML
    with open(os.path.join(output_folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved main HTML from {base_url}")

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract CSS + JS links
    resources = []

    # CSS files
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href")
        if href:
            resources.append(urljoin(base_url, href))

    # JS files
    for script in soup.find_all("script", src=True):
        src = script.get("src")
        if src:
            resources.append(urljoin(base_url, src))

    # Download resources
    for resource_url in resources:
        download_file(session, resource_url, output_folder)

if __name__ == "__main__":
    website_url = "https://tortillaco-leuven.be/"  
    scrape_website(website_url)
