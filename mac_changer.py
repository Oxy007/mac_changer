#!/usr/bin/env python

import subprocess
import optparse

import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please provide interface name, or use -- help.")
    elif not options.new_mac:
        parser.error("[-] Please provide interface new MAC address, or use --help")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC Address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Sorry I could not read the MAC address")


options = get_arguments()
current_mac = get_mac_address(options.interface)
print("[+] Current MAC is > " + str(current_mac))
change_mac(options.interface, options.new_mac)

current_mac = get_mac_address(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address changed " + current_mac)
else:
    print("[-] MAC address did not changed")
