import subprocess
import requests

from rich import print as r_print

#API toke from netbox
headers = {"Authorization": "Token 529a3b0fc593b17fd8f5f02b2211bf0908c7c26c",
           "Content-Type": "application/json",
           "Accept": "application/json"}


ip_address = "192.168.21.216" #nexan storage unit (NXS-E18-DC-E-R3-U15-TRS)

def is_ip_reachable(ip):
    # Windows ping: -n 1
    # Linux ping: -c 1
    command = ["ping", "-n", "1", ip]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


output = is_ip_reachable(ip_address)
    
if output:
        response= requests.patch("https://10.250.11.12/api/dcim/devices/39/", headers=headers,verify=False,json={"custom_fields": {"Status": True}}) #updates only the required field to true
        print(output)
        r_print(response)
        r_print(response.json())
else:
         response= requests.patch("https://10.250.11.12/api/dcim/devices/39/", headers=headers,verify=False,json={"custom_fields": {"Status": False}}) #updates only the required field to true   
         print(output)
         r_print(response)
         r_print(response.json())