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

def get_wireless_interfaces():
    result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
    output_lines = result.stdout.splitlines()
    interfaces = []
    for line in output_lines:
        if "Interface" in line:
            interface = line.split()[-1]
            interfaces.append(interface)
    return interfaces

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
        file_name = os.path.basename(__file__)
        wireless_interfaces = get_wireless_interfaces()

        monitor = ["1", "01", "mon", "monitor", "mntr", "mo", "mntor", "mont"]
        managed = ["2", "02", "managed", "man", "ma", "mngd", "mangd", "mnged", "mang"]
        spoof = ["3", "03", "spoof", "spf", "sp" , "sf"]
        status = ["4", "04", "status", "st", "stus", "sts", "stts", "sttus", "stats"]

        help = ['0', '00', '--help', '/help', '-h', '/h', '-?', '/?']
        lists = ['--list', '/list', '-l', '/l']

        modes = [monitor, managed, spoof, status]

        if len(sys.argv) > 3:
            print("\nUsage:")
            print("\tchange <interface> <mode>")
            sys.exit(1)

        elif (sys.argv[1] in help and len(sys.argv) == 2):
            print("\nchange <interface> <mode>:")
            print("\n   Modes:")
            print("\tRoot permissions:")
            print("\t[01] - Monitor   | Switches your wireless itnerface into monitor mode")
            print("\t[02] - Managed   | Switches your wireless interface into managed mode")
            print("\t[03] - Spoof     | Spoofs your mac address")
            print("\n\tNon-Root permissions:")
            print("\t[04] - Status    | Gives you informations about your wireless interface")
            print("\n\tExample: change <interface> --status")
            print("\n   Options:")
            print("\t[00] - Help      | Prints this help")
            print("\t[99] - List      | Lists your wireless interfaces")
            print("\n\tExample: change --help")
            print(f"\n{file_name} - Made by: S4W77")
            sys.exit(1)

        elif (sys.argv[1] in lists and len(sys.argv) == 2):
            interface_count = len(list(enumerate(wireless_interfaces)))
            if interface_count == 1:
                print("\nWireless Interface:")
            elif interface_count == 0:
                print("\nNo wireless interface was found.")
                sys.exit(1)
            else:
                print("\nWireless Interfaces:")
            for idx, interface in enumerate(wireless_interfaces, start=1):
                if idx < 10:
                    print(f"\t[0{idx}] - {interface}")
                elif idx >= 10:
                    print(f"\t[{idx}] - {interface}")
            sys.exit(1)

        iface = sys.argv[1]
        mode = sys.argv[2].strip().lower()

        if not check_interface_exists(iface) and any(mode in sublist for sublist in modes):
            print(f"\nInterface '{iface}' not found.")
            sys.exit(1)
        elif not check_interface_exists(iface) and any(mode not in sublist for sublist in modes):
            iface = sys.argv[2]
            mode = sys.argv[1]
            if not check_interface_exists(iface) and any(mode in sublist for sublist in modes):
                print(f"\nInterface '{iface}' not found.")
                sys.exit(1)

        try:
            iw_output = os.popen('iw dev').read()

            if mode in monitor:

                if 'Interface' in iw_output and 'monitor' not in iw_output:
                    check_root()
                    os.system(f'airmon-ng check kill > /dev/null 2>&1')
                    os.system(f'ifconfig {iface} down > /dev/null 2>&1')
                    os.system(f'macchanger -r {iface} > /dev/null 2>&1')
                    os.system(f'iw dev {iface} set type monitor > /dev/null 2>&1')
                    os.system(f'ifconfig {iface} up > /dev/null 2>&1')
                    print(f'\n{iface} is successfully set in monitor mode.\nSpoodef mac: {get_interface_mac(iface)}')
                    sys.exit(1)

                else:
                    os.system(f'ifconfig {iface} down > /dev/null 2>&1')
                    os.system(f'macchanger -r {iface} > /dev/null 2>&1')
                    os.system(f'ifconfig {iface} up > /dev/null 2>&1')
                    print("\nInterface already in monitor mode.\nSpoodef mac: {get_interface_mac(iface)}")
                    sys.exit(1)

            elif mode in managed:

                if 'Interface' in iw_output and 'managed' not in iw_output:
                    check_root()
                    os.system(f'ifconfig {iface} down > /dev/null 2>&1')
                    os.system(f'macchanger -r {iface} > /dev/null 2>&1')
                    os.system(f'iw dev {iface} set type managed > /dev/null 2>&1')
                    os.system(f'ifconfig {iface} up > /dev/null 2>&1')
                    os.system(f'service NetworkManager restart > /dev/null 2>&1')
                    print(f'\n{iface} is successfully set in managed mode.\nSpoodef mac: {get_interface_mac(iface)}')
                    sys.exit(1)

                else:
                    os.system(f'ifconfig {iface} down > /dev/null 2>&1')
                    os.system(f'macchanger -r {iface} > /dev/null 2>&1')
                    os.system(f'ifconfig {iface} up > /dev/null 2>&1')
                    print("\nInterface already in managed mode.\nSpoodef mac: {get_interface_mac(iface)}")
                    sys.exit(1)

            elif mode in spoof:
                os.system(f'ifconfig {iface} down > /dev/null 2>&1')
                os.system(f'macchanger -r {iface} > /dev/null 2>&1')
                os.system(f'ifconfig {iface} up > /dev/null 2>&1')
                print(f"\nInterface: {iface}\nMode: {get_interface_mode(iface)}\nSpoofed mac: {get_interface_mac(iface)}")
                sys.exit(1)

            elif mode in status:
                print("\nphy#1")
                print(f"\tInterface: {iface}")
                print(f"\tMode: {get_interface_mode(iface)}")
                print(f"\tMac: {get_interface_mac(iface)}")
                print(f"\tIP: {get_interface_info(iface)}")
                sys.exit(1)

            else:
                print("\nInvalid usage. Please use '--help' to see the usage.")
                sys.exit(1)

        except Exception as e:
            print(f"\nFailed to set {iface} in {mode} mode. Error: {e}.")
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

# Credits to S4W77
