from extras.scripts import Script, ObjectVar
from dcim.models import Device
import subprocess


class PingAndUpdateCF(Script):
    class Meta:
        name = "Ping and Update Custom Field"

    device = ObjectVar(
        model=Device,
        required=True,
        description="Select a device"
    )

    def run(self, data, commit=True):
        device = data["device"]

        if not device.primary_ip:
            self.log_failure("Device has no primary IP")
            return

        ip = str(device.primary_ip.address).split("/")[0]

        result = subprocess.call(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ) == 0

        # API-equivalent update
        device.custom_field_data = {
            **device.custom_field_data,
            "status": bool(result),  # or "Test"
        }

        if commit:
            device.save()

        self.log_success(
            f"{device.name} ({ip}) reachable={result}"
        )
