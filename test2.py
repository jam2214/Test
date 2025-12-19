import subprocess
from extras.scripts import Script
from dcim.models import Device

class PingUpdateStatus(Script):
    class Meta:
        name = "Ping & Update Status"

    ip_address = "8.8.8.8"  # Hardcoded for now

    def run(self, data, commit=True):

        def is_ip_reachable(ip):
            command = ["ping", "-c", "1", ip]
            return subprocess.call(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ) == 0

        result = is_ip_reachable(self.ip_address)

        device = Device.objects.first()  # safer than hardcoding ID

        device.custom_field_data["status"] = result

        if commit:
            device.save()

        self.log_success(f"Ping result: {result}")
