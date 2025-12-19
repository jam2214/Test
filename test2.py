import subprocess

from extras.scripts import Script, ObjectVar
from dcim.models import Device


class PingUpdateStatus(Script):
    class Meta:
        name = "Ping & Update Status (Custom Field)"
        description = "Ping device primary IPv4 and update boolean custom field 'status'"

    device = ObjectVar(
        model=Device,
        required=True,
        description="Device to ping"
    )

    def run(self, data, commit=True):
        device = data["device"]

        if not device.primary_ip4:
            self.log_failure("Device has no primary IPv4 address")
            return

        ip = str(device.primary_ip4.address.ip)

        try:
            result = subprocess.call(
                ["ping", "-c", "1", "-W", "1", ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ) == 0
        except Exception as e:
            self.log_failure(f"Ping failed to execute: {e}")
            return

        # REQUIRED BY USER: custom_field_data assignment
        device.custom_field_data["status"] = result

        if commit:
            device.save()

        self.log_success(
            f"{device.name} ({ip}) is {'UP' if result else 'DOWN'}"
        )
