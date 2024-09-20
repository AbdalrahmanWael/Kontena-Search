from fasthtml.common import *
import sqlite3
from crawler import crawl

body_style = "font-family: 'Pixelify Sans', cursive;"
tailwind = Script(src="https://cdn.tailwindcss.com")
font = Style("""@import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400..700&display=swap');""")
favicon = Favicon(light_icon='favicon.ico', dark_icon='favicon.ico')
app = FastHTMLWithLiveReload(hdrs=(tailwind, font, favicon))

def search_database(query):
    conn = sqlite3.connect('search_engine.db')
    c = conn.cursor()
    words = query.split()
    placeholders = ','.join(['?'] * len(words))
    c.execute(f"""
        SELECT p.url, p.title, p.content, SUM(w.frequency) as relevance
        FROM pages p
        JOIN words w ON p.id = w.page_id
        WHERE w.word IN ({placeholders})
        GROUP BY p.id
        ORDER BY relevance DESC
        LIMIT 10
    """, words)
    results = c.fetchall()
    conn.close()
    return results

@app.get('/')
def get():
    return generate_home_page()

@app.post('/')
def post(SearchInput: str = ""):
    return RedirectResponse(f"/search?q={SearchInput}", status_code=303)

@app.get('/search')
def get_search(q: str = ""):
    return generate_results_page(q)

@app.post('/search')
def post_search(SearchInput: str = ""):
    return RedirectResponse(f"/search?q={SearchInput}", status_code=303)

def generate_home_page():
    return (
        Title("Kontena"),
        Body(
            Div(
                Img(src="Kontena.svg", cls="w-full md:w-3/4 mb-6"),
                Form(
                    Input(type="text", name="SearchInput", placeholder="Search",
                          cls='outline-none bg-transparent rounded-2xl border-2 border-red-800 focus:border-red-600 hover:border-red-600 p-3 transition-all text-white text-xl w-full'),  
                    Div(
                        Button("I'm feeling lucky", cls='bg-red-700 select-none text-white px-4 py-2 rounded-lg mt-4 hover:bg-red-800 transition-all'),
                        Button("Kontena Search", type="submit", cls='bg-red-700 select-none text-white px-4 py-2 rounded-lg mt-4 hover:bg-red-800 transition-all'),
                        cls='flex gap-4')
                    , cls='w-full flex flex-col items-center gap-4', method="post", action="/"),
            cls='w-full md:w-1/2 flex flex-col items-center gap-10 p-5 md:p-2'),  
            cls='bg-[#08001a] min-h-screen flex items-center justify-center text-red-800', style=body_style
        )
    )

def generate_results_page(query):
    query = query.lower()
    results = search_database(query) if query else []

    search_bar = Form(
        Div(
            A(Img(src="Kontena.svg", cls="h-8 mr-4 hidden md:block"), href="/"),
            Input(type="text", name="SearchInput", value=query,
                  cls='outline-none bg-transparent rounded-2xl border-2 border-red-800 focus:border-red-600 hover:border-red-600 p-2 transition-all text-white text-lg flex-grow'),
            Button("Search", type="submit", cls='bg-red-700 select-none text-white px-4 py-2 rounded-lg ml-2 hover:bg-red-800 transition-all'),
            cls='flex items-center w-full max-w-4xl'
        ),
        cls='mb-8', method="post", action="/search"
    )

    search_results = Div(
        H2(f"Search Results for '{query}':", cls="text-xl font-bold mb-4 text-red-600"),
        *(
            Div(
                A(result[1], href=result[0], cls="text-xl text-blue-500 hover:underline visited:text-purple-600"),
                Div(result[0], cls="text-green-500 text-sm mb-1"),
                P(result[2][:200] + "...", cls="text-gray-300"),
                cls="mb-6"
            ) for result in results
        )
    ) if results else Div(f"No results found for '{query}'", cls="text-red-600")

    return (
        Title(f"Kontena - {query}"),
        Body(
            Div(
                search_bar,
                search_results,
                Div(A(Img(src="Kontena.svg", cls="h-8 mr-4"), href="/"), cls="w-full flex justify-end"),
                cls='w-full max-w-4xl mx-auto p-4 '
            ),
            cls='bg-[#08001a] min-h-screen text-red-800', style=body_style
        )
    )

@app.get('/add_url')
def get_add_url():
    return Body(
        Form(
            Input(type="url", name="url", placeholder="Enter URL to crawl"),
            Button("Add URL", type="submit")
        )
    )

@app.post('/add_url')
def post_add_url(url: str):
    crawl(url, depth=1)  # Crawl just this URL
    return Body(f"Added and crawled: {url}")

@app.get('/admin/crawl')
def get_admin_crawl():
    return Body(
        Form(
            Input(type="url", name="start_url", placeholder="Start URL"),
            Input(type="number", name="depth", placeholder="Crawl Depth"),
            Button("Start Crawling", type="submit")
        )
    )

@app.post('/admin/crawl')
def post_admin_crawl(start_url: str, depth: int):
    crawl(start_url, depth)
    return Body(f"Crawling started from {start_url} with depth {depth}")

@app.get("/{fname:path}.{ext:static}")
def static(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

serve()