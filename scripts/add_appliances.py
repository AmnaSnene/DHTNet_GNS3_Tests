import json
import subprocess
import requests

# install https://downloads.openwrt.org/releases/23.05.0/targets/x86/64/openwrt-23.05.0-x86-64-generic-ext4-combined.img.gz
subprocess.run(["wget", "https://downloads.openwrt.org/releases/23.05.0/targets/x86/64/openwrt-23.05.0-x86-64-generic-ext4-combined.img.gz", "-o", ""])
subprocess.run(["gunzip", "openwrt-23.05.0-x86-64-generic-ext4-combined.img.gz"])

# install qemu
subprocess.run(["sudo", "apt-get", "install", "qemu"])


# add openWRT appliance
# POST http://192.168.56.1:3080/v2/templates {'compute_id': 'vm', 'name': 'OpenWrt 22.03.0', 'usage': 'Ethernet0 is the LAN link, Ethernet1 the WAN link, Ethernet2 and Ethernet3 are optional links.', 'category': 'router', 'symbol': ':/symbols/classic/router.svg', 'template_type': 'qemu', 'adapter_type': 'virtio-net-pci', 'adapters': 4, 'console_type': 'telnet', 'hda_disk_interface': 'ide', 'ram': 128, 'hda_disk_image': 'openwrt-22.03.0-x86-64-generic-ext4-combined.img', 'qemu_path': '/usr/bin/qemu-system-x86_64'}
openWRT_data = {'compute_id': 'vm', 'name': 'OpenWrt 23.05.0', 'usage': 'Ethernet0 is the LAN link, Ethernet1 the WAN link, Ethernet2 and Ethernet3 are optional links.', 'category': 'router', 'symbol': ':/symbols/classic/router.svg', 'template_type': 'qemu', 'adapter_type': 'virtio-net-pci', 'adapters': 4, 'console_type': 'telnet', 'hda_disk_interface': 'ide', 'ram': 128, 'hda_disk_image': 'openwrt-23.05.0-x86-64-generic-ext4-combined.img', 'qemu_path': '/usr/bin/qemu-system-x86_64'}
response = requests.post(url = "http://192.168.56.1:3080/v2/templates", data = json.dumps(openWRT_data))
print(response.text)

# add webterm appliance
# POST POST http://192.168.56.1:3080/v2/templates {'compute_id': 'vm', 'name': 'webterm', 'usage': 'The /root directory is persistent.', 'category': 'guest', 'symbol': 'firefox.svg', 'template_type': 'docker', 'adapters': 1, 'console_type': 'vnc', 'image': 'gns3/webterm:latest', 'template_id': 'feeb7ea2-4145-4481-a11f-319d21856ed7'}
webterm_data = {'compute_id': 'vm', 'name': 'webterm', 'usage': 'The /root directory is persistent.', 'category': 'guest', 'symbol': 'firefox.svg', 'template_type': 'docker', 'adapters': 1, 'console_type': 'vnc', 'image': 'gns3/webterm:latest'}
response = requests.post(url = "http://192.168.56.1:3080/v2/templates", data = json.dumps(webterm_data))
print(response.text)