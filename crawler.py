import requests
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin

def setup_database():
    conn = sqlite3.connect('search_engine.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pages
                 (id INTEGER PRIMARY KEY, url TEXT UNIQUE, title TEXT, content TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS words
                 (word TEXT, page_id INTEGER, frequency INTEGER,
                 FOREIGN KEY(page_id) REFERENCES pages(id))''')
    conn.commit()
    return conn

def crawl(url, depth=2):
    visited = set()
    to_visit = [(url, 0)]
    
    conn = setup_database()
    c = conn.cursor()

    while to_visit:
        current_url, current_depth = to_visit.pop(0)
        print('current url: ', current_url)
        
        if current_url in visited or current_depth > depth:
            continue
        
        visited.add(current_url)
        
        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.title.string if soup.title else "No title"
            content = soup.get_text()
            
            # Store page in database
            c.execute("INSERT OR IGNORE INTO pages (url, title, content) VALUES (?, ?, ?)",
                      (current_url, title, content))
            page_id = c.lastrowid
            
            # Simple word frequency
            words = content.lower().split()
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Store word frequencies
            for word, freq in word_freq.items():
                c.execute("INSERT INTO words (word, page_id, frequency) VALUES (?, ?, ?)",
                          (word, page_id, freq))
            
            # Find links for further crawling
            if current_depth < depth:
                for link in soup.find_all('a', href=True):
                    new_url = urljoin(current_url, link['href'])
                    to_visit.append((new_url, current_depth + 1))
            
            conn.commit()
            
        except Exception as e:
            print(f"Error crawling {current_url}: {e}")
    
    conn.close()

if __name__ == "__main__":
    start_url = "https://en.wikipedia.org/wiki/John_von_Neumann" 
    crawl(start_url, depth=200)
