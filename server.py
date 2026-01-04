import json
import http.server
import socketserver
import os
import re
from http import HTTPStatus

from model.repositories.driver_repository import DriverRepository
from model.repositories.freight_repository import FreightRepository
from model.repositories.region_repository import RegionRepository
from model.repositories.freight_type_repository import FreightTypeRepository

from controller.driver_controller import DriverController
from controller.freight_controller import FreightController
from controller.region_controller import RegionController
from controller.freight_type_controller import FreightTypeController
from controller.dashboard_controller import DashboardController

PORT = 8000

driver_repo = DriverRepository()
freight_repo = FreightRepository()
region_repo = RegionRepository()
freight_type_repo = FreightTypeRepository()

driver_controller = DriverController(driver_repo)
freight_controller = FreightController(freight_repo)
region_controller = RegionController(region_repo)
freight_type_controller = FreightTypeController(freight_type_repo)

dashboard_controller = DashboardController(
    freight_repo,
    region_repo,
    driver_repo,
    freight_type_repo
)


class RequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith("/api/drivers"):
            self.send_json(driver_controller.get_all())
            return

        elif self.path.startswith("/api/freights"):
            self.send_json(freight_controller.get_all())
            return

        elif self.path.startswith("/api/regions"):
            self.send_json(region_controller.get_all())
            return

        elif self.path.startswith("/api/freight_types"):
            self.send_json(freight_type_controller.get_all())
            return

        elif self.path.startswith("/api/dashboard/kpis"):
            self.send_json(dashboard_controller.get_kpis())
            return

        elif self.path.startswith("/api/dashboard/freight_by_region"):
            self.send_json(dashboard_controller.get_freight_volume_by_region())
            return

        elif self.path.startswith("/api/dashboard/delay_by_region"):
            self.send_json(dashboard_controller.get_delay_rate_by_region())
            return

        elif self.path.startswith("/api/dashboard/driver_performance"):
            self.send_json(dashboard_controller.get_driver_performance())
            return

        elif self.path.startswith("/api/dashboard/revenue_vs_delay"):
            self.send_json(dashboard_controller.get_revenue_vs_delay_by_freight_type())
            return

        # 🔽 SÓ CHEGA AQUI SE NÃO FOR API
        if self.path == "/" or self.path == "/index.html":
            self.path = "/view/index.html"

        elif not self.path.startswith("/view"):
            potential_path = "/view" + self.path
            if os.path.exists(os.getcwd() + potential_path):
                self.path = potential_path

        super().do_GET()


    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON")
            return

        if self.path == "/api/drivers":
            new_driver = driver_controller.create(data)
            self.send_json(new_driver, HTTPStatus.CREATED)

        elif self.path == "/api/freights":
            new_freight = freight_controller.create(data)
            self.send_json(new_freight, HTTPStatus.CREATED)

        else:
            self.send_error(HTTPStatus.NOT_FOUND)


    def do_DELETE(self):
        driver_match = re.match(r"/api/drivers/(\d+)", self.path)
        freight_match = re.match(r"/api/freights/(\d+)", self.path)

        if driver_match:
            id = int(driver_match.group(1))
            if driver_controller.delete(id):
                self.send_response(HTTPStatus.NO_CONTENT)
                self.end_headers()
            else:
                self.send_error(HTTPStatus.NOT_FOUND)

        elif freight_match:
            id = int(freight_match.group(1))
            if freight_controller.delete(id):
                self.send_response(HTTPStatus.NO_CONTENT)
                self.end_headers()
            else:
                self.send_error(HTTPStatus.NOT_FOUND)

        else:
            self.send_error(HTTPStatus.NOT_FOUND)


    def send_json(self, data, status=HTTPStatus.OK):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))



print(f"Server running at http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    httpd.serve_forever()
