import http.server
import socketserver
import re
from jinja2 import Template

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler


class MyHandler(Handler):
    template = Template(open('template/player.html').read())

    def render_template(self, asset_id):
        html = self.template.render(asset_id=asset_id)
        return html

    def do_GET(self):
        if re.match(r'/player/(?P<asset_id>[a-z0-9-]+)', self.path):
            asset_id = re.search(r'/player/(?P<asset_id>[a-z0-9-]+)', self.path).group('asset_id')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(self.render_template(asset_id), "utf8"))
        elif re.match(r'/render/(?P<sku>[a-z0-9-]+)', self.path):
            sku = re.search(r'/render/(?P<sku>[a-z0-9-]+)', self.path).group('sku')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(bytes(f'Hello {sku}', "utf8"))
        else:
            super().do_GET()


httpd = socketserver.TCPServer(("", PORT), MyHandler)
print("Server started at port: ", PORT)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()
    print("Server stopped.")