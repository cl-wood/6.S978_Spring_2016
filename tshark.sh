#!/bin/bash

#cp wifi.pcap temp.pcap
tshark -nr wifi.pcap -o wlan.enable_decryption:TRUE -o "uat:80211_keys:\"wpa-psk\",\" 95bc9770d399d8180e8cb93098724b91e3cebb13800d0d3e161dd2773da48fbc\"" -Y "http"
