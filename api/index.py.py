# api/index.py
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import os

# Load marking data from JSON file
def load_marking_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'marking_data.json'), 'r') as f:
        return json.load(f)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Load marking data
        MARKING_DATA = load_marking_data()

        # Parse query parameters
        query_params = parse_qs(self.path.split('?')[-1] if '?' in self.path else '')
        names = query_params.get('name', [])

        # Get marks from custom data
        marks = [MARKING_DATA.get(name, 0) for name in names]

        # Prepare response
        response = json.dumps({"marks": marks})
        self.wfile.write(response.encode())
        return