# GNS3 Tests

GNS3 (Graphical Network Simulator-3) can be used in the context of Jami to create virtual environments to test Jami networking features such as peer discovery, PUPnP, etc. GNS3 is open-source, free software with a large community and complete [documentation](#https://docs.gns3.com/docs/).

## SetUp
GNS3 consists of two components:
- GUI: Graphical client (There is also a web client but in my understanding it's very limited on linux plateform)
- Server: The server can be hosted on localhost, a local VM, or a remote virtual machine. The VM was originally introduced for Windows and Mac hosts, but it is recommended to use the VM even on Linux.

The GUI and the VM should be on the same version. To change the VM version, you need to select the upgrade section on the VM and choose the GUI version.


To add the VM to your GUI, click  edit -> preference -> GNS3 VM.

To add Wizard - server to your GUI (required for cisco devices), fellow this [tutorial](https://docs.gns3.com/docs/getting-started/setup-wizard-local-server).


## Add docker container:
To add docker container, you need first to add the template: click edit -> preference -> Doker container templates -> new
If the Docker image already exists on Docker Hub, GNS3 will pull it for you; otherwise, you need to make sure that the image exists on the VM.

## Networking
Before starting the VM, you need to add a network adapter. You can create multiple adapters (you need a NAT adapter).
To create a virtual network deployed on the VM, use the NAT node or the Cloud node with a port of the network adapter set to NAT or Bridged (NOT host-only).

## REST API:
For REST API documentation, refer to the [REST API Documentation](https://gns3-server.readthedocs.io/en/stable/endpoints.html)
[Swagger version](https://gns3-server.readthedocs.io/en/stable/endpoints.html)


First check the controller address associated to 3080 port (default port):
```sh
ss -tuln
```
To enable/disable the authentification, click edit -> preference ->server -> Protect server with password.


GNS3 has a consol. It can be very useful to adjust the debug level and read the log since the UI is using the same API to communicate with the controller.

## Ressources:
- [Videos](https://www.youtube.com/watch?v=Ibe3hgP8gCA)
- [API wrapper](https://github.com/davidban77/gns3fy)
- [Ansible tutorial](https://davidban77.hashnode.dev/automate-your-network-labs-with-ansible-and-gns3-part-2-ck2kprqem00asnos1l89dp07k?source=more_articles_bottom_blogs)

## Establishing Multiple Networks Using a pFsense router

By default, the pFsense router allocates port em1 to the primary LAN. To set up an extra LAN, it's necessary to attach a new interface to a port, assign a static IP address and IP range. Remember to activate DHCP for this newly created LAN.


TODO: record video / add more details