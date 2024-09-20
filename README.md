# Kontena Search Engine
<div align="center">
![Kontena](Kontena.svg)</div>
Kontena is a lightweight, customizable search engine built with FastHTML. It features a simple, pixel-art inspired interface and allows users to search through a database of crawled web pages.

## Features

- Clean, minimalist user interface with a pixel art aesthetic
- Full-text search functionality
- Web crawler for adding new pages to the search index
- Admin interface for initiating crawls
- Responsive design that works on both desktop and mobile devices

## Requirements

- Python 3.7+
- FastHTML library
- SQLite3

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/kontena-search.git
   cd kontena-search
   ```

2. Install the required dependencies:
   ```
   pip install fasthtml sqlite3
   ```

3. Set up the SQLite database:
   ```
   sqlite3 search_engine.db < schema.sql
   ```

## Usage

1. Start the server:
   ```
   python main.py
   ```

2. Open a web browser and navigate to `http://localhost:8000`

3. Use the search bar to find content in the indexed pages

## Adding Content

There are two ways to add content to the search index:

1. Single URL:
   - Navigate to `http://localhost:8000/add_url`
   - Enter a URL and submit the form

2. Bulk crawl (admin only):
   - Navigate to `http://localhost:8000/admin/crawl`
   - Enter a starting URL and crawl depth
   - Submit the form to start the crawl

## Customization

- Modify the `body_style` variable in `main.py` to change the font
- Update the `Kontena.svg` file to change the logo
- Adjust the color scheme by modifying the Tailwind classes in the HTML generation functions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
