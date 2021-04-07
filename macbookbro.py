#!/usr/bin/env python3

import subprocess
import optparse
import re

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_result =  str(ifconfig_result)
    mac_add_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_add_search:
        return mac_add_search.group(0)
    else:
        print("[-] Couldn't get MAC-Address.")


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="The interface to change the MAC Address")
    parser.add_option("-m", "--mac", dest="new_mac", help="The New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] No interface specified. Use --help for more.")
    elif not options.new_mac:
        parser.error("[-] No MAC Address given. Use --help for more")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC to " + new_mac + " on " + interface )
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("[!] Current MAC Address = " + str(current_mac))

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print("[+] MAC Address changed successfully to " + current_mac)
else:
    print("[-] MAC Addresss couldn't be changed.")