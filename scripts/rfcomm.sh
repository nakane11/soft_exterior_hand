#!/bin/bash
read -sp "Password: " password
echo "$password"  | sudo -S rfcomm bind 0 08:B6:1F:EE:38:26
sudo chmod a+rw /dev/rfcomm0

roslaunch soft_exterior_hand hand.launch
