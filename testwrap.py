import subprocess
from extras.scripts import Script, ObjectVar
from dcim.models import Device

class PingUpdateStatus(Script):
    class Meta:
        name = "Ping & Update Status"
        description = "Ping a device and update its status custom field"

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

        ip = device.primary_ip.address.ip.exploded

        # --- ping function ---
        def is_ip_reachable(ip):
            command = ["ping", "-c", "1", ip]
            return subprocess.call(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ) == 0

        result = is_ip_reachable(ip)

        # --- update NetBox object ---
        device.custom_field_data["status"] = "UP" if result else "DOWN"

        if commit:
            device.save()

        self.log_success(
            f"{device.name} ({ip}) is {'UP' if result else 'DOWN'}"
        )
