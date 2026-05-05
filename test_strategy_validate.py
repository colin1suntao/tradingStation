#!/usr/bin/env python3
import requests

code_content = """
class Strategy:
    def __init__(self, params=None):
        pass
    def initialize(self, context):
        pass
    def on_bar(self, data):
        return {"signal": "hold"}
"""

response = requests.post(
    "http://localhost:8000/api/v1/strategies/validate",
    params={"code_content": code_content}
)

print("Status Code:", response.status_code)
print("Response:", response.text)
