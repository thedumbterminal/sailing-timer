# LAN Config

On the pi:

sudo nmcli connection modify "netplan-eth0" \
  ipv4.method manual \
  ipv4.addresses 10.0.0.1/24 

sudo nmcli connection modify "netplan-eth0" \
  802-3-ethernet.mac-address ""

sudo nmcli connection up "netplan-eth0"

sudo nmcli device status

ssh -l pi 10.0.0.1
