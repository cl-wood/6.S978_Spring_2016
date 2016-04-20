#!/bin/bash

sudo tcpdump -I -ni en1 -w wifi.pcap
#sudo tcpdump -I -l -ni en1 -w wifi.pcap
