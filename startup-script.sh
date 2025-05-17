#!/bin/bash

# Create VPP log directory
mkdir -p /var/log/vpp

# Start VPP in the background
/usr/bin/vpp -c /etc/vpp/startup.conf &
vpp_pid=$!

# Start FRR
/usr/lib/frr/frrinit.sh start

# Wait for VPP to exit (or keep container running)
wait $vpp_pid
