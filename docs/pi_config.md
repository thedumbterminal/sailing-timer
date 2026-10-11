# PI Config

apt-get install x11-utils

## Access point

sudo nmcli connection add \
  type wifi \
  ifname wlan0 \
  con-name PiHotspot \
  ssid Sailing-App \
  802-11-wireless.mode ap \
  802-11-wireless.band bg \
  ipv4.method shared \
  ipv6.method disabled \
  ipv4.addresses 192.168.50.1/24

sudo nmcli connection down PiHotspot
sudo nmcli connection up PiHotspot

