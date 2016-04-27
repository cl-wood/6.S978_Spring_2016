# Clark Wood -- MIT 6.S978, Spring 2016
# Usage: sudo python2.7 demo.py
# 5) Send HTTP GET request
import base64, os, requests, signal, subprocess, time

with open('./passwd.txt', 'r') as read_file:
    password = read_file.read()

print '\n\n\nIs this your password: {}?\n\n\n'.format(password)

# Take picture
pic_file = 'pic.jpeg'
while 1:
    i = raw_input('Shall we take a picture?\n')
    r = requests.post('http://10.255.255.1/image/jpeg.cgi', auth=('admin', password))
    with open(pic_file, 'wb') as f:
        r.raw.decode_content = True
        f.write(r.content)
        print '\nWrote file to: {}\n'.format(pic_file)

