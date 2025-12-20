from extras.scripts import Script, ObjectVar
from dcim.models import Device


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

        self.log_success(
            f"Selected device: name={device.name}, id={device.id}"
        )
