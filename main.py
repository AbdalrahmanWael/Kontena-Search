from fasthtml.common import *

app, rt = fast_app()

@rt("/")
def get():
    return Titled("Kontena Search", P("Let's do this!"))

serve()