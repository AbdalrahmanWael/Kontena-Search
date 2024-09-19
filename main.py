from fasthtml.common import *

body_style = "font-family: 'Pixelify Sans', cursive;"
tailwind = Script(src="https://cdn.tailwindcss.com")
font = Style("""@import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400..700&display=swap');""")
favicon = Favicon(light_icon='favicon.ico',dark_icon='favicon.ico')
app = FastHTMLWithLiveReload(hdrs=(tailwind, font, favicon))

@app.get('/')
def get():
    page = ( 
    Title("Kontena"), 
    Body(
        Div(
            Img(src="Kontena.svg", cls="w-full md:w-3/4 mb-6"), 
            Form(
               Input(type="text", name="SearchInput", placeholder="Search",
                     cls='outline-none bg-transparent rounded-2xl border-2 border-red-800 focus:border-red-600 hover:border-red-600 p-3 transition-all text-white text-xl w-full '),  
              Div( 
                Button("I'm feeling lucky", cls='bg-red-700 text-white px-4 py-2 rounded-lg mt-4 hover:bg-red-800 transition-all')
                , 
                  Button("Kontena Search", type="submit", cls='bg-red-700 text-white px-4 py-2 rounded-lg mt-4 hover:bg-red-800 transition-all') 
                 ,cls='flex gap-4' )
            , cls='w-full flex flex-col items-center gap-4')
        ,cls='w-full md:w-1/2 flex flex-col items-center gap-10 p-5 md:p-2'),  
        cls='bg-[#08001a] w-screen h-screen flex items-center justify-center text-red-800', style=body_style) 
    )
    return page 

@app.get("/{fname:path}.{ext:static}")
def static(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

serve()
