# GNS3 Tests

GNS3 (Graphical Network Simulator-3) can be utilized with Jami to create virtual environments for testing Jami networking features such as peer discovery and PUPnP. GNS3 is an open-source, free software with extensive [documentation](#https://docs.gns3.com/docs/).

## Setup
GNS3 comprises two components:
- GUI: Graphical client (There is also a web client, but it is quite limited on Linux platforms)
- Server: The server can be hosted on localhost, a local VM, or a remote virtual machine. Although the VM was initially introduced for Windows and Mac hosts, it is recommended to use the VM even on Linux.

Ensure the GUI and the VM are on the same version. To change the VM version, go to the upgrade section on the VM and select the GUI version.

To add the VM to your GUI, navigate to edit -> preferences -> GNS3 VM.

To add the Wizard - server to your GUI (required for Cisco devices), follow this [tutorial](https://docs.gns3.com/docs/getting-started/setup-wizard-local-server).

## Adding Docker Containers
To add a Docker container, first add the template: navigate to edit -> preferences -> Docker container templates -> new. If the Docker image is available on Docker Hub, GNS3 will pull it for you; otherwise, ensure the image exists on the VM.

## Networking
To add a Host-only Adapter: open VirtualBox > go to Tools > click the icon of 3 lines on the rightmost side of the toolbar > click network options > click create.

Before starting the VM, add a network adapter. You can create multiple adapters (a NAT adapter and a bridged adapter are needed). To create a virtual network on the VM, use the NAT node or the Cloud node with a network adapter port set to NAT or Bridged (NOT host-only). Set up the local GNS3 Wizard.

Verify the host-only adapter of your VM and obtain its IP address using the command `ip addr show <adapter_name>`. This IP address will be required for the REST API.


## REST API
For REST API documentation, refer to the [REST API Documentation](https://gns3-server.readthedocs.io/en/stable/endpoints.html) and the [Swagger version](https://gns3-server.readthedocs.io/en/stable/endpoints.html).

First, check the controller address associated with port 3080 (default port):
```sh
ss -tuln
```
To enable/disable authentication, navigate to edit -> preferences -> server -> Protect server with password.

GNS3 has a console that can be very useful for adjusting the debug level and reading logs since the UI uses the same API to communicate with the controller.

## Resources
- [Videos](https://www.youtube.com/watch?v=Ibe3hgP8gCA)
- [API wrapper](https://github.com/davidban77/gns3fy)
- [Ansible tutorial](https://davidban77.hashnode.dev/automate-your-network-labs-with-ansible-and-gns3-part-2-ck2kprqem00asnos1l89dp07k?source=more_articles_bottom_blogs)

# Scripts
In the `scripts` directory, there are three scripts:

* `install_gns3.sh`: Installs GNS3 UI, GNS3 VM, adds GNS3 VM to VirtualBox, and integrates the GNS3 VM with GNS3 using the GNS3 REST API.
* `add_appliances.py`: Adds templates for OpenWrt and Webterm appliances, making them available in the VM for future use. This script uses the REST API.
* `update_dhtnet_appliances.py`: Creates a project and adds a DHTNet appliance using a Docker URL from GitHub. The template is downloaded and updated in the VM. The script then deletes the project, ensuring the DHTNet appliance is available in the VM for future use.

# OpenWrt
Setting up UPnP in OpenWrt: [OpenWrt UPnP Setup](https://openwrt.org/docs/guide-user/firewall/upnp/upnp_setup#setting_up_upnp_in_openwrt)

Update the package list and install miniupnpd:
```sh
opkg update
opkg install miniupnpd
```
