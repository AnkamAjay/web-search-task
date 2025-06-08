import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse, urlunparse

def normalize_url(url):
    parsed = urlparse(url)
    normalized = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=parsed.netloc.lower(),
        path=parsed.path.rstrip('/')
    )
    return urlunparse(normalized)

class WebCrawler:
    def __init__(self):
        self.index = defaultdict(list)
        self.visited = set()

    def crawl(self, url, base_url=None):
        normalized_url = normalize_url(url)
        if normalized_url in self.visited:
            return
        self.visited.add(normalized_url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.index[url] = soup.get_text()

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    if urlparse(href).netloc:
                        href = urljoin(base_url or url, href)
                    absolute_url = urljoin(base_url or url, href)
                    normalized_absolute_url = normalize_url(absolute_url)
                    if normalized_absolute_url not in self.visited and normalized_absolute_url.startswith(base_url or url):
                        self.crawl(normalized_absolute_url, base_url=base_url or url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")


    def search(self, keyword):
        results = []
        for url, text in self.index.items():
            if keyword.lower() in text.lower():
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}")
        else:
            print("No results found.")

def main():
    crawler = WebCrawler()
    start_url = "https://example.com"
    crawler.crawl(start_url)

    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)

if __name__ == "__main__":
    main()
