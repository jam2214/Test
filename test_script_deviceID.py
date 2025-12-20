from extras.scripts import Script, ObjectVar
from dcim.models import Device
import subprocess


class ShowDeviceInfo(Script):
    class Meta:
        name = "Show Device Info (Test Script)"
        description = "Displays the selected device name and ID"

    device = ObjectVar(
        model=Device,
        required=True,
        description="Select a device"
    )

    def run(self, data, commit=True):
        device = data["device"]

        primary_ip = (
            str(device.primary_ip.address).split("/")[0]
            if device.primary_ip
            else "N/A"
        )
        result = subprocess.call(
            ["ping", "-c", "1", "-W", "1", primary_ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ) == 0

        self.log_success(
            f"Selected device: name={device.name}, id={device.id}, ip={primary_ip}"
        )
        self.log_success(
            f"Selected device: name={device.name} ({primary_ip}) is {'UP' if result else 'DOWN'}"
        )




