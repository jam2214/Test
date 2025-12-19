import subprocess

from extras.scripts import Script, StringVar
from dcim.models import Device


class PingUpdateStatus(Script):
    class Meta:
        name = "Ping & Update Status (Custom Field)"

    device_name = StringVar(
        required=True,
        description="Device name (passed from custom link)"
    )

    def run(self, data, commit=True):
        device_name = data["device_name"]

        try:
            device = Device.objects.get(name=device_name)
        except Device.DoesNotExist:
            self.log_failure(f"Device '{device_name}' not found")
            return

        if not device.primary_ip4:
            self.log_failure("Device has no primary IPv4 address")
            return

        ip = str(device.primary_ip4.address).split("/")[0]

        result = subprocess.call(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ) == 0

        device.custom_field_data["status"] = result

        if commit:
            device.save()

        self.log_success(
            f"{device.name} ({ip}) is {'UP' if result else 'DOWN'}"
        )
