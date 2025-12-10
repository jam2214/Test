# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 16:57:17 2025

@author: janalbert.mostert
"""

from extras.scripts import Script
import subprocess
import requests

class UpdateDeviceStatus(Script):
    class Meta:
        name = "Update Device Status"

    # Optional input variables can be added here if needed
    ip_address = "192.168.21.216"  # Replace with actual IP

    def run(self, data, commit=True):
        headers = {
            "Authorization": "Token 529a3b0fc593b17fd8f5f02b2211bf0908c7c26c",  # Your NetBox API token
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        def is_ip_reachable(ip):
            # Linux ping: -c 1
            command = ["ping", "-n", "1", ip]
            return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

        output = is_ip_reachable(self.ip_address)

        device_id = 39  # DCIM device ID to update

        if output:
            
            payload = {"custom_fields": {"Status": True}}

            url = f"https://10.250.11.12/api/dcim/devices/{device_id}/"

            response = requests.patch(url, headers=headers, verify=False, json=payload)

            self.log_info(f"Ping result: {output}")
            self.log_info(f"Response: {response.status_code} {response.text}")

        else:
            payload = {"custom_fields": {"Status": False}}

            url = f"https://10.250.11.12/api/dcim/devices/{device_id}/"

            response = requests.patch(url, headers=headers, verify=False, json=payload)

            self.log_info(f"Ping result: {output}")
            self.log_info(f"Response: {response.status_code} {response.text}")
            

