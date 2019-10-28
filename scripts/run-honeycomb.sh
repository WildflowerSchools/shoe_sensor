#!/bin/bash

python -m shoe_sensor.tools.collect_honeycomb -m mac_addresses.txt -c 0 -l INFO -t 5 -a $(cat /boot/wildflower-config.yml | yq -r .device_id) -e capucine
