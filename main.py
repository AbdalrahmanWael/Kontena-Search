from fasthtml.common import *

body_style = "max-width: 700px; background-color: lavender; font-family: 'Short Stack', cursive;"
tailwind = Script(src="https://cdn.tailwindcss.com")
font = Style("""@import url('https://fonts.googleapis.com/css2?family=Short+Stack&display=swap');""")
app = FastHTML(hdrs=(tailwind, font))

@app.get('/')
def get():
    page = ( 
    Title("Kontena"), 
    Body(
        Titled("Kontena Search", P("Let's do this!"), Div(Img(src="Kontena.svg")),
            Div(
               Form(Input(type="text", name="SearchInput", placeholder="Search"), Button("Search", type="submit"))
            )
        ), cls='bg-gray-800', style=body_style)
    )
    return page 

@app.get("/{fname:path}.{ext:static}")
def static(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

serve()
