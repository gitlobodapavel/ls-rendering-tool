import http.server
import socketserver
import re
import time

from driver import Driver
import services

PORT = 8001
Handler = http.server.SimpleHTTPRequestHandler


class MyHandler(Handler):

    def do_GET(self):
        if re.match(r'/render/(?P<sku>[a-z0-9-]+)', self.path):
            sku = re.search(r'/render/(?P<sku>[a-z0-9-]+)', self.path).group('sku')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            asset_id = services.sku_to_id(sku)

            if not asset_id:
                self.wfile.write(bytes(f'the {sku} product does not have a vray configurator', "utf8"))
                return

            driver = Driver()
            try:
                driver.get_page(asset_id)

                attributes = driver.get_attributes()

                materials = services.get_materials(attributes)
                layers = services.get_layers(attributes, services.get_composite(asset_id))

                services.start_render_job(materials, layers, asset_id, services.get_stage_id(asset_id))

                self.wfile.write(bytes(f'render job for {sku} started', "utf8"))
            except Exception as e:
                # driver.close()
                self.wfile.write(bytes(f'server error {e}', "utf8"))
        else:
            super().do_GET()


httpd = socketserver.TCPServer(("", PORT), MyHandler)
print("API started at port: ", PORT)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()
    print("API stopped.")