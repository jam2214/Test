#import subprocess
#from extras.scripts import Script
#from dcim.models import Device

#class PingUpdateStatus(Script):
 #   class Meta:
  #      name = "Ping & Update Status"

   # ip_address = "8.8.8.8"  # Hardcoded for now

    #def run(self, data, commit=True):

        # --- ping function ---
     #   def is_ip_reachable(ip):
      #      command = ["ping", "-c", "1", ip]  # Linux
       #     return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

        #result = is_ip_reachable(self.ip_address)

        # --- update NetBox object directly through ORM ---
       # device = Device.objects.get(id=39)
       # device.custom_field_data["Status"] = result
       # device.save()

        #self.log_success(f"Ping result: {result}")
from extras.scripts import Script, ObjectVar
from dcim.models import Device
import subprocess

class PingDevice(Script):
    class Meta:
        name = "Ping Device"
        description = "Ping a device and update status"

    device = ObjectVar(
        model=Device,
        required=True
    )

    def run(self, data, commit=True):
        device = data["device"]

        if not device.primary_ip:
            self.log_failure("No primary IP set")
            return

        ip = device.primary_ip.address.ip.exploded

        reachable = subprocess.call(
            ["ping", "-c", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ) == 0

        device.custom_field_data["status"] = "UP" if reachable else "DOWN"

        if commit:
            device.save()

        self.log_success(f"{device.name} is {'UP' if reachable else 'DOWN'}")



