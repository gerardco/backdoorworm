from subprocess import *
c = ['ls','-l']
handle = Popen(c,stdin=PIPE, stderr=PIPE,stdout=PIPE,shell=True)
print handle.stdout.read()
handle.flush()
