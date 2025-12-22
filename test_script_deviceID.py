from extras.scripts import Script, ObjectVar
from dcim.models import Device
import subprocess


class ShowDeviceInfo(Script):
    class Meta:
        name = "Ping IP & Update Cusom Field (Script)"
        description = "Ping a device from custom link and get status from ping"

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
        oob_ip = (
            str(device.oob_ip.address).split("/")[0]
            if device.oob_ip
            else "N/A"
        )

        primary_ip_result = subprocess.call(
            ["ping", "-c", "1", "-W", "1", primary_ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ) == 0
        
        oob_ip_result = subprocess.call(
            ["ping", "-c", "1", "-W", "1", primary_ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ) == 0
        

        if oob_ip_result:
            device.custom_field_data["Status"] = True
        else:
            device.custom_field_data["Status"] = False

        if commit:
            device.save()

        self.log_success(
            f"Primary IP: name={device.name}, id={device.id}, ip={primary_ip} is {'UP' if primary_ip_result else 'DOWN'}"
        )
        self.log_success(
            f"Out-Of-Band IP: name={device.name}, id={device.id}, ip={oob_ip_result} is {'UP' if oob_ip_result else 'DOWN'}"
        )
 





