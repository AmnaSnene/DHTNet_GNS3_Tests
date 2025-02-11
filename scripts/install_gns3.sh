#!/bin/bash

# This script installs GNS3 on Debian-based systems.
# It also downloads and imports the GNS3 VM into VirtualBox.
# The GNS3 VM is configured with 4 CPUs, 8GB of RAM, and a NAT adapter.
# The script also adds the GNS3 VM to GNS3 using the GNS3 REST API.
# The user is prompted to reboot the system after the installation is complete.

# Update package lists
echo "Updating package lists..."
sudo apt-get update

# Install dependencies
echo "Installing dependencies..."
sudo apt-get install -y software-properties-common

# Add GNS3 PPA
echo "Adding GNS3 PPA..."
sudo add-apt-repository -y ppa:gns3/ppa

# Update package lists again
echo "Updating package lists after adding GNS3 PPA..."
sudo apt-get update

# Install GNS3 GUI and server
echo "Installing GNS3 GUI and server..."
sudo apt-get install -y gns3-gui gns3-server

# Install additional recommended packages
echo "Installing additional recommended packages..."
sudo apt-get install -y wireshark
sudo apt-get install -y ubridge
sudo apt-get install -y vpcs

# Set permissions for Wireshark
echo "Setting permissions for Wireshark..."
sudo dpkg-reconfigure wireshark-common
sudo usermod -aG wireshark $USER

# Allow non-root users to use GNS3
echo "Allowing non-root users to use GNS3..."
sudo usermod -aG ubridge $USER
sudo usermod -aG libvirt $USER
sudo usermod -aG kvm $USER

# Install VirtualBox
echo "Installing VirtualBox..."
sudo apt-get install -y virtualbox

# Add user to vboxusers group
echo "Adding user to vboxusers group..."
sudo usermod -aG vboxusers $USER

# Download GNS3 VM for VirtualBox
echo "Downloading GNS3 VM..."
# use a our version of GNS3 VM:
#   2 Networks adaptors: Host-only and NAT
#   6 CPUs
#   16GB RAM (maybe more)
GNS3_VM_URL="https://github.com/GNS3/gns3-gui/releases/download/v2.2.48.1/GNS3.VM.VirtualBox.2.2.48.1.zip"

wget $GNS3_VM_URL -O /tmp/GNS3_VM.zip

# Install unzip if not already installed
echo "Installing unzip..."
sudo apt-get install -y unzip

# Extract GNS3 VM
echo "Extracting GNS3 VM..."
unzip /tmp/GNS3_VM.zip -d /tmp/GNS3_VM

# Import GNS3 VM into VirtualBox
echo "Importing GNS3 VM into VirtualBox..."
VBoxManage import /tmp/GNS3_VM/GNS3\ VM.ova

# Cleanup
rm /tmp/GNS3_VM.zip
rm -rf /tmp/GNS3_VM

echo "REBOOT YOUR SYSTEM NOW"

# Install curl if not already installed
echo "Installing curl..."
sudo apt-get install -y curl

# Adjust GNS3 VM settings
echo "Adjusting GNS3 VM settings..."
VBoxManage modifyvm "GNS3 VM" --cpus 4 --memory 8192 --vram 12

VBoxManage modifyvm "GNS3 VM" --nested-hw-virt on


# Add NAT adapter to GNS3 VM
echo "Adding NAT adapter to GNS3 VM..."
VBoxManage modifyvm "GNS3 VM" --nic1 nat

# Start the VM
echo "Starting GNS3 VM..."
VBoxManage startvm "GNS3 VM" --type headless

# Wait for the VM to boot
echo "Waiting for GNS3 VM to boot..."
sleep 20

# It is possible that you need to add DNS servers to the sudo nano /etc/systemd/resolved.conf, e.g.: nameserver 8.8.8.8
# It is also possible that you need to install some dependencies manually
# Then start the GNS3 server manually: sudo gns3restore
# You can follow these steps:
# echo "Running commands inside the GNS3 VM..."
# echo 'DNS=8.8.8.8 1.1.1.1' | sudo tee -a /etc/systemd/resolved.conf
# echo 'FallbackDNS=8.8.4.4 1.0.0.1' | sudo tee -a /etc/systemd/resolved.conf
# sudo systemctl restart systemd-resolved
# sudo apt-get update
# sudo apt-get install plymouth-themes plymouth-label
# sudo gns3restore


# Add GNS3 VM to GNS3
# Change the host IP
# Any valid ID following the same format can be used for compute_id
curl -X POST \
  http://localhost:3080/v2/computes \
  -H "Content-Type: application/json" \
  -d '{
    "host": "192.168.56.106",
    "name": "GNS3 VM",
    "user": "gns3",
    "password": "gns3",
    "protocol": "http",
    "port": 80.
    "compute_id": "d09fd215-bb61-43e9-8288-820cc09813y6"
  }'

if [ $? -eq 0 ]; then
  echo "GNS3 VM added successfully."
else
  echo "Failed to add GNS3 VM."
  echo "Please add the GNS3 VM manually."
  # Inform the user about the need to add DNS servers and install dependencies manually
  echo "Please check if the GNS3 server is running on the GNS3 VM."
  echo "If not, please follow these steps to configure the GNS3 server on the GNS3 VM:"
  echo "1. Run the following commands inside the GNS3 VM:"
  echo '   echo "DNS=8.8.8.8 1.1.1.1" | sudo tee -a /etc/systemd/resolved.conf'
  echo '   echo "FallbackDNS=8.8.4.4 1.0.0.1" | sudo tee -a /etc/systemd/resolved.conf'
  echo '   sudo systemctl restart systemd-resolved'
  echo '   sudo apt-get update'
  echo '   sudo apt-get install plymouth-themes plymouth-label'
  echo '   sudo gns3restore'
  echo "2. Install any additional dependencies manually."
fi
# Inform the user about the need to reboot
echo "Please reboot your system to apply all changes."
