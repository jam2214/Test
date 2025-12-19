import subprocess
from extras.scripts import Script, ObjectVar
from dcim.models import Device
from ipam.models import IPAddress
from utilities.form import DynamicModelChoiceField


class PingUpdateStatus(Script):
    class Meta:
        name = "Ping & Update Status"

    device = ObjectVar(
        model=Device,
        required=True,
        description="Device to ping"
    )

    def run(self, data, commit=True):
        device = data["device"]

        if not device.primary_ip:
            self.log_failure("Device has no primary IP")
            return

        ip = str(device.primary_ip4.address.ip)

        result = subprocess.call(
            ["ping", "-c", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ) == 0

        device.custom_field_data["status"] = result

        if commit:
            device.save()

        self.log_success(
            f"{device.name} ({ip}) is {'UP' if result else 'DOWN'}"
        )

