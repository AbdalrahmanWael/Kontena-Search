
<div align="center">
  <img src="Kontena.svg" alt="Kontena Logo">
</div>



**Kontena** is a lightweight, customizable search engine built using FastHTML. It features a simple, pixel-art-inspired interface and allows users to search through a database of crawled web pages.

## Features

- Clean, minimalist user interface with a pixel-art aesthetic
- Full-text search functionality
- Web crawler for adding new pages to the search index
- Admin interface for initiating web crawls
- Responsive design for both desktop and mobile devices

## Requirements

- Python 3.7+
- FastHTML library
- SQLite3

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/kontena-search.git
   cd kontena-search
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:
   ```bash
   python main.py
   ```

2. Open a web browser and navigate to `http://localhost:8000`.

3. Use the search bar to find content from the indexed pages.

## Adding Content to the Search Index

You can add content to the search index in two ways:

1. **Single URL Submission**:
   - Go to `http://localhost:8000/add_url`
   - Enter the desired URL and submit the form

2. **Bulk Crawl (Admin Only)**:
   - Go to `http://localhost:8000/admin/crawl`
   - Enter a starting URL and specify the crawl depth
   - Submit the form to initiate the web crawl

## Customization

- To change the font, modify the `body_style` variable in `main.py`.
- To change the logo, replace or edit the `Kontena.svg` file.
- To adjust the color scheme, modify the Tailwind CSS classes in the HTML generation functions.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit a Pull Request. We encourage improvements, feature additions, and bug fixes.

## License

This open-source project is available under the [MIT License](LICENSE).
