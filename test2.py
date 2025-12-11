import subprocess
from extras.scripts import Script
from dcim.models import Device

class PingUpdateStatus(Script):
    class Meta:
        name = "Ping & Update Status"

    ip_address = "192.168.21.216"  # Hardcoded for now

    def run(self, data, commit=True):

        # --- ping function ---
        def is_ip_reachable(ip):
            command = ["ping", "-c", "1", ip]  # Linux
            return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

        result = is_ip_reachable(self.ip_address)

        # --- update NetBox object directly through ORM ---
        device = Device.objects.get(id=39)
        device.custom_field_data["Status"] = result
        device.save()

        self.log_success(f"Ping result: {result}")

