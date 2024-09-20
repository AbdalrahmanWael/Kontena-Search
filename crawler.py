import requests
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin, urlparse
import time
import re
import logging
from collections import deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_database():
    conn = sqlite3.connect('search_engine.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pages
                 (id INTEGER PRIMARY KEY, url TEXT UNIQUE, title TEXT, content TEXT, 
                 description TEXT, keywords TEXT, last_crawled TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS words
                 (word TEXT, page_id INTEGER, frequency INTEGER,
                 FOREIGN KEY(page_id) REFERENCES pages(id))''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_words_word ON words(word)')
    conn.commit()
    return conn

def get_metadata(soup):
    description = ""
    keywords = ""
    
    description_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    if description_tag:
        description = description_tag.get('content', '')
    
    keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
    if keywords_tag:
        keywords = keywords_tag.get('content', '')
    
    return description, keywords

def clean_text(text):
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', text)).strip().lower()

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def crawl_page(url, depth, conn, base_domain):
    try:
        logger.info(f"Crawling: {url} (Depth: {depth})")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else "No title"
        content = clean_text(soup.get_text())
        description, keywords = get_metadata(soup)
        
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO pages (url, title, content, description, keywords, last_crawled) VALUES (?, ?, ?, ?, ?, datetime('now'))",
                  (url, title, content, description, keywords))
        page_id = c.lastrowid
        
        words = content.split()
        word_freq = {}
        for word in words:
            if len(word) > 1:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        c.executemany("INSERT INTO words (word, page_id, frequency) VALUES (?, ?, ?)",
                      [(word, page_id, freq) for word, freq in word_freq.items()])
        
        conn.commit()
        
        new_urls = []
        if depth > 0:
            for link in soup.find_all('a', href=True):
                new_url = urljoin(url, link['href'])
                if is_valid_url(new_url) and urlparse(new_url).netloc == base_domain:
                    new_urls.append((new_url, depth - 1))
        
        logger.info(f"Finished crawling: {url} (Found {len(new_urls)} new URLs)")
        return new_urls
    
    except Exception as e:
        logger.error(f"Error crawling {url}: {e}")
        return []

def crawl(start_url, depth=2, max_pages=100):
    visited = set()
    to_visit = deque([(start_url, depth)])
    base_domain = urlparse(start_url).netloc
    
    conn = setup_database()
    
    try:
        while to_visit and len(visited) < max_pages:
            url, current_depth = to_visit.popleft()
            
            if url not in visited:
                visited.add(url)
                new_urls = crawl_page(url, current_depth, conn, base_domain)
                
                for new_url in new_urls:
                    if new_url[0] not in visited:
                        to_visit.append(new_url)
                
                logger.info(f"Crawled {len(visited)} pages. Remaining to visit: {len(to_visit)}")
                time.sleep(0.1)
    
    except KeyboardInterrupt:
        logger.info("Crawling interrupted by user")
    
    finally:
        conn.close()
        logger.info(f"Crawling completed. Total pages crawled: {len(visited)}")

if __name__ == "__main__":
    start_url = "https://en.wikipedia.org/wiki/John_von_Neumann"
    # start_url = "https://docs.fastht.ml/"
    crawl(start_url, depth=4, max_pages=500)
