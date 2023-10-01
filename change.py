#!/usr/bin/python

import os
import sys
import subprocess

def check_root():
    if not os.geteuid() == 0:
        print("\nYou must run this script with root privileges.")
        sys.exit(1)

def check_interface_exists(interface):
    return os.path.exists(f"/sys/class/net/{interface}")

def get_interface_mode(interface):
    try:
        output = subprocess.check_output(["iwconfig", interface]).decode("utf-8")
        lines = output.split('\n')
        for line in lines:
            if "Mode:" in line:
                mode = line.split("Mode:")[1].split()[0]
                return mode
        return "Not Available"
    except subprocess.CalledProcessError:
        return "Error: Interface not found"

def get_interface_mac(interface):
    try:
        output = subprocess.check_output(["ip", "link", "show", interface]).decode("utf-8")
        lines = output.split('\n')
        for line in lines:
            if "link/ether" in line:
                mac_address = line.split("link/ether")[1].strip().split()[0]
                return mac_address
        return "Not Available"
    except subprocess.CalledProcessError:
        return "Error: Interface not found"

def get_interface_info(interface):
    try:
        output = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
        for line in output.split('\n'):
            if "inet " in line:
                ip_address = line.split('inet ')[1].split()[0]
                return ip_address
        return "Not Available"
    except subprocess.CalledProcessError:
        return "Not Available"

def function():
    try:
        if len(sys.argv) > 3:
            print("\nUsage:")
            print("\tchange <interface> <mode>")
            sys.exit(1)

        elif (sys.argv[1] in ['0', '00', '--help', '/help', '-h', '/h', '-?', '/?'] and len(sys.argv) == 2):
                print("\nchange <interface> <mode>:")
                print("\n\t0 - Help (does not require an interface)")
                print("\t1 - Monitor")
                print("\t2 - Managed")
                print("\t3 - Status")
                sys.exit(1)

        iface = sys.argv[1]
        mode = sys.argv[2].strip().lower()

        if not check_interface_exists(iface):
            iface = sys.argv[2]
            mode = sys.argv[1]
            if not check_interface_exists(iface) and ((mode in ["1", "01", "mon", "monitor", "mntr", "mo", "mntor", "mont"]) or (mode in ["2", "02", "managed", "man", "ma", "mngd", "mangd", "mnged", "mang"])):
                print(f"\nInterface '{iface}' not found.")
                sys.exit(1)

        try:
            iw_output = os.popen('iw dev').read()

            if mode in ["1", "01", "mon", "monitor", "mntr", "mo", "mntor", "mont"]:

                if 'Interface' in iw_output and 'monitor' not in iw_output:
                    check_root()
                    os.system(f'airmon-ng check kill > /dev/null 2>&1')
                    os.system(f'ifconfig {iface} down > /dev/null 2>&1')
                    os.system(f'iw dev {iface} set type monitor > /dev/null 2>&1')
                    os.system(f'ifconfig {iface} up > /dev/null 2>&1')
                    print(f'\n{iface} is successfully set in monitor mode.')
                    sys.exit(1)

                else:
                    print("\nInterface already in monitor mode.")
                    sys.exit(1)

            elif mode in ["2", "02", "managed", "man", "ma", "mngd", "mangd", "mnged", "mang"]:

                if 'Interface' in iw_output and 'managed' not in iw_output:
                    check_root()
                    os.system(f'ifconfig {iface} down > /dev/null 2>&1')
                    os.system(f'iw dev {iface} set type managed > /dev/null 2>&1')
                    os.system(f'ifconfig {iface} up > /dev/null 2>&1')
                    os.system(f'service NetworkManager restart > /dev/null 2>&1')
                    print(f'\n{iface} is successfully set in managed mode.')
                    sys.exit(1)

                else:
                    print("\nInterface already in managed mode.")
                    sys.exit(1)

            elif mode in ["3", "03", "status", "st", "stus", "sts", "stts", "sttus", "stats", "s"]:
                print("\nphy#1")
                print(f"\tInterface: {iface}")
                print(f"\tMode: {get_interface_mode(iface)}")
                print(f"\tMac: {get_interface_mac(iface)}")
                print(f"\tIP: {get_interface_info(iface)}")
                sys.exit(1)

            else:
                print("\nInvalid mode. Use 'mon or man' to change the interface mode.")
                sys.exit(1)

        except Exception as e:
            print(f"\nFailed to set {iface} in monitor mode. Error: {e}.")
            sys.exit(1)
    except IndexError:
        print("\nNo prefix was added! Use change /? for help")
        sys.exit(1)
try:
    if __name__ == "__main__":
        function()

except KeyboardInterrupt:
    print("\nOperation aborted by user.")
    sys.exit(1)
