import http.server
import socketserver
import urllib.parse
import wikipedia

# Konfigurasi Wikipedia
wikipedia.set_lang("id")

class WikipediaHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        keyword = query_params.get('keyword', ['Python Programming'])[0]
        html_content = self.generate_html(keyword)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def generate_html(self, keyword):
        try:
            # Dapatkan artikel Wikipedia
            summary = wikipedia.summary(keyword, sentences=8)
        except wikipedia.exceptions.DisambiguationError as e:
            summary = f"Terjadi ambiguitas untuk '{keyword}'. Pilihan: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            summary = f"Tidak ditemukan artikel untuk '{keyword}'"
        except Exception as e:
            summary = f"Error: {str(e)}"

        # HTML template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Wikipedia App</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .search {{ margin-bottom: 20px; }}
                input[type="text"] {{ padding: 10px; width: 300px; }}
                button {{ padding: 10px 15px; }}
                .article {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>Wikipedia Article Generator</h1>
            <div class="search">
                <form method="GET">
                    <input type="text" name="keyword" value="{keyword}" placeholder="Cari artikel...">
                    <button type="submit">Cari</button>
                </form>
            </div>
            <div class="article">
                <h2>{keyword}</h2>
                <p>{summary}</p>
            </div>
        </body>
        </html>
        """
        return html

# Jalankan server
if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(("", PORT), WikipediaHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()
