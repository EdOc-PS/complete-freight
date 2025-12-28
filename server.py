import json
import http.server
import socketserver
import os
import re
from http import HTTPStatus
from typing import Tuple, Optional

from model.repositories.driver_repository import DriverRepository
from model.repositories.freight_repository import FreightRepository
from model.repositories.region_repository import RegionRepository
from model.repositories.freight_type_repository import FreightTypeRepository
from controller.driver_controller import DriverController
from controller.freight_controller import FreightController
from controller.region_controller import RegionController
from controller.freight_type_controller import FreightTypeController
from controller.dashboard_controller import DashboardController

# Import main to update dashboard data
# try:
#     from main import main as update_dashboard
# except ImportError:
#     print("Warning: Could not import main.py, dashboard won't auto-update.")
#     def update_dashboard(): pass

PORT = 8000

# Initialize components
driver_repo = DriverRepository("data/drivers.json")
freight_repo = FreightRepository("data/freights.json")
region_repo = RegionRepository("data/regions.json")
freight_type_repo = FreightTypeRepository("data/freight_types.json")

driver_controller = DriverController(driver_repo)
freight_controller = FreightController(freight_repo)
region_controller = RegionController(region_repo)
freight_type_controller = FreightTypeController(freight_type_repo)
dashboard_controller = DashboardController(freight_repo, region_repo, driver_repo, freight_type_repo)

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path.startswith("/api/drivers"):
            self.send_json(driver_controller.get_all())
        elif self.path.startswith("/api/freights"):
            self.send_json(freight_controller.get_all())
        elif self.path.startswith("/api/regions"):
            self.send_json(region_controller.get_all())
        elif self.path.startswith("/api/freight_types"):
            self.send_json(freight_type_controller.get_all())
        elif self.path.startswith("/api/dashboard/kpis"):
            self.send_json(dashboard_controller.get_kpis())
        elif self.path.startswith("/api/dashboard/freight_by_region"):
            self.send_json(dashboard_controller.get_freight_volume_by_region())
        elif self.path.startswith("/api/dashboard/delay_by_region"):
            self.send_json(dashboard_controller.get_delay_rate_by_region())
        elif self.path.startswith("/api/dashboard/driver_performance"):
            self.send_json(dashboard_controller.get_driver_performance())
        elif self.path.startswith("/api/dashboard/revenue_vs_delay"):
            self.send_json(dashboard_controller.get_revenue_vs_delay_by_freight_type())
        else:
            # Static file serving logic
            if self.path == "/" or self.path == "/index.html":
                self.path = "/view/index.html"
            
            # Check if it's a request for data
            elif self.path.startswith("/data/"):
                # Check root data folder
                if os.path.exists(os.getcwd() + self.path):
                    pass # path is already correct relative to root
                # Check view/data folder
                elif os.path.exists(os.getcwd() + "/view" + self.path):
                    self.path = "/view" + self.path
            
            # Check if it's other static assets (js, css, assets)
            # Usually these are inside view/
            elif not self.path.startswith("/view"):
                 potential_path = "/view" + self.path
                 if os.path.exists(os.getcwd() + potential_path):
                     self.path = potential_path
            
            # SimpleHTTPRequestHandler serves relative to CWD based on self.path
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
             self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON")
             return

        if self.path == "/api/drivers":
            new_driver = driver_controller.create(data)
            self.send_json(new_driver, HTTPStatus.CREATED)
            # try: update_dashboard() 
            # except Exception as e: print(f"Error updating dashboard: {e}")
        elif self.path == "/api/freights":
            new_freight = freight_controller.create(data)
            self.send_json(new_freight, HTTPStatus.CREATED)
            # try: update_dashboard() 
            # except Exception as e: print(f"Error updating dashboard: {e}")
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def do_DELETE(self):
        # Regex to match /api/drivers/123
        driver_match = re.match(r"/api/drivers/(\d+)", self.path)
        freight_match = re.match(r"/api/freights/(\d+)", self.path)

        if driver_match:
            id = int(driver_match.group(1))
            if driver_controller.delete(id):
                self.send_response(HTTPStatus.NO_CONTENT)
                self.end_headers()
                # try: update_dashboard() 
                # except Exception as e: print(f"Error updating dashboard: {e}")
            else:
                self.send_error(HTTPStatus.NOT_FOUND)
        elif freight_match:
            id = int(freight_match.group(1))
            if freight_controller.delete(id):
                self.send_response(HTTPStatus.NO_CONTENT)
                self.end_headers()
                # try: update_dashboard() 
                # except Exception as e: print(f"Error updating dashboard: {e}")
            else:
                self.send_error(HTTPStatus.NOT_FOUND)
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def send_json(self, data, status=HTTPStatus.OK):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

print(f"Server started at http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    httpd.serve_forever()
