import http.server
import socketserver
import urllib.parse
import wikipedia
import traceback

# Konfigurasi Wikipedia
wikipedia.set_lang("id")

class WikipediaHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            keyword = query_params.get('keyword', ['Python Programming'])[0]
            html_content = self.generate_html(keyword)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Server Error: {str(e)}")
    
    def generate_html(self, keyword):
        try:
            # Dapatkan artikel Wikipedia
            summary = wikipedia.summary(keyword, sentences=8)
            title = keyword
        except wikipedia.exceptions.DisambiguationError as e:
            summary = f"Terjadi ambiguitas untuk '{keyword}'. Pilihan: {', '.join(e.options[:5])}"
            title = f"Disambiguation: {keyword}"
        except wikipedia.exceptions.PageError:
            summary = f"Tidak ditemukan artikel untuk '{keyword}'. Coba kata kunci lain."
            title = f"Not Found: {keyword}"
        except Exception as e:
            summary = f"Error: {str(e)}"
            title = f"Error: {keyword}"

        # HTML template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Wikipedia App - {title}</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 40px;
                    line-height: 1.6;
                }}
                .search {{ 
                    margin-bottom: 20px;
                    padding: 20px;
                    background: #f0f0f0;
                    border-radius: 8px;
                }}
                input[type="text"] {{ 
                    padding: 10px; 
                    width: 300px; 
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }}
                button {{ 
                    padding: 10px 15px; 
                    background: #007cba;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }}
                button:hover {{
                    background: #005a87;
                }}
                .article {{ 
                    background: #f9f9f9; 
                    padding: 20px; 
                    border-radius: 8px;
                    border-left: 4px solid #007cba;
                }}
                h1 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h1>📚 Wikipedia Article Generator</h1>
            <div class="search">
                <form method="GET">
                    <input type="text" name="keyword" value="{keyword}" placeholder="Cari artikel Wikipedia...">
                    <button type="submit">🔍 Cari</button>
                </form>
            </div>
            <div class="article">
                <h2>{title}</h2>
                <p>{summary}</p>
            </div>
        </body>
        </html>
        """
        return html

# Jalankan server
if __name__ == "__main__":
    PORT = 8000
    try:
        with socketserver.TCPServer(("", PORT), WikipediaHandler) as httpd:
            print(f"🚀 Server running at http://localhost:{PORT}")
            print("📍 Access: http://localhost:8000/?keyword=Indonesia")
            print("⏹️  Press Ctrl+C to stop")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
