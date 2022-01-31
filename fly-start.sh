#/bin/sh
DNS_LISTEN_ADDRESS=`getent hosts fly-global-services|awk '{print $1}'` ./dns.py
