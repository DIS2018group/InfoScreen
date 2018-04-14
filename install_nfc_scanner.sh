#!/bin/bash
echo "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"1da8\", ATTRS{idProduct}==\"1301\", ACTION==\"add\", MODE=\"0704\"" > /etc/udev/rules.d/99-nfcscanner.rules
