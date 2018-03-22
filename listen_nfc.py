import binascii
import pyudev
import time

from users import login_user, logout_user


EMPTY_LINE = b'\x00' * 32


def discover_device():
    ctx = pyudev.Context()

    for device in ctx.list_devices().match(subsystem="hidraw"):
        if "1DA8:1301" in device.sys_path:
            return device.device_node

    return None


def listen_to_device(device_path):
    with open(device_path, "rb") as f:
        while True:
            output = f.read(32)

            if output == EMPTY_LINE:
                continue

            output = str(binascii.hexlify(output), "utf-8")

            if output.startswith("0201"):
                # Tag placed on the scanner
                tag_id = output[10:]
                print("Tag %s placed on scanner" % tag_id)

                user_id = "NFC:%s" % tag_id
                login_user("NFC", user_id)
            elif output.startswith("0202"):
                # Tag removed from the scanner
                print("Tag removed from scanner")
                logout_user("NFC")

if __name__ == "__main__":
    device_path = discover_device()

    if not device_path:
        raise IOError("Couldn't find the device.")

    listen_to_device(device_path)
