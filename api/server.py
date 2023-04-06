import http.server
import json
import socketserver
import re

from driver import Driver
import services
from jinja2 import Template

PORT = 8001
Handler = http.server.SimpleHTTPRequestHandler


class MyHandler(Handler):
    exists = Template(open('templates/exists.html').read())
    started = Template(open('templates/started.html').read())
    error = Template(open('templates/error.html').read())

    def do_GET(self):
        if re.match(r'/render/(?P<sku>[a-z0-9-]+)', self.path):
            sku = re.search(r'/render/(?P<sku>[a-z0-9-]+)', self.path).group('sku')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            if re.search(r'(\?|\&)force=true', self.path):
                pass
            else:
                check_job = services.read_job(sku)
                if check_job:

                    message = {"status": "failed",
                    "message": f"job for sku: {sku} has already been created earlier",
                    "details": f"https://preview.threekit.com/o/livingspacessandbox/jobs/{check_job['job_id']}"}

                    html = self.exists.render(message=message, link=f'http://127.0.0.1:8001/render/{sku}?force=true')
                    self.wfile.write(bytes(html, "utf8"))
                    """self.wfile.write(bytes(json.dumps({"status": "failed",
                                                       "message": f"job for sku: {sku} has already been created earlier",
                                                       "details": f"https://preview.threekit.com/o/livingspacessandbox/jobs/{check_job['job_id']}"}).encode()))"""
                    return

            asset_id = services.sku_to_id(sku)

            if not asset_id:
                # self.wfile.write(bytes(f'the {sku} product does not have a vray configurator', "utf8"))
                message = {"status": "failed", "details": f"item with sku: {sku} does not have a vray configurator"}
                html = self.error.render(message=message)
                self.wfile.write(bytes(html, "utf8"))
                return

            driver = Driver()
            try:
                driver.get_page(asset_id)

                attributes = driver.get_attributes()

                materials = services.get_materials(attributes)
                layers = services.get_layers(attributes, services.get_composite(asset_id))

                job_id = services.start_render_job(materials, layers, asset_id, services.get_stage_id(asset_id))

                message = {"status": "success",
                           "message": "render-vray job started",
                           "details": f"https://preview.threekit.com/o/livingspacessandbox/jobs/{job_id}"}
                html = self.started.render(message=message)
                self.wfile.write(bytes(html, "utf8"))

                services.save_job(job_id=job_id, sku=sku, asset_id=asset_id)
            except Exception as e:
                # driver.close()
                self.wfile.write(bytes(json.dumps({"status": "failed",
                                                   "message": "server error",
                                                   "details": f"{e}"}).encode()))
        else:
            super().do_GET()


httpd = socketserver.TCPServer(("", PORT), MyHandler)
print("API started at port: ", PORT)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()
    print("API stopped.")