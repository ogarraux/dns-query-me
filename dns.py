#!/usr/bin/env python

import os
import time
import logging

from dnslib.server import DNSServer, BaseResolver
from dnslib import RR, QTYPE, RCODE, A

logging.basicConfig(level="DEBUG")


class IPResolver(BaseResolver):
    def __init__(self, answer_for):
        self.answer_for = answer_for

    def resolve(self, request, handler):
        reply = request.reply()
        if request.q.qname == self.answer_for:
            ip = handler.client_address
            logging.warning(f"Query from {ip}")
            reply.add_answer(RR(request.q.qname, QTYPE.A, ttl=60, rdata=A(ip[0])))
        else:
            reply.header.rcode = RCODE.NXDOMAIN
        return reply


DNS_ANSWER_FOR = os.environ.get("DNS_ANSWER_FOR", "myip.example.com")
DNS_LISTEN_PORT = int(os.environ.get("DNS_LISTEN_PORT", 53))
DNS_LISTEN_ADDRESS = os.environ.get("DNS_LISTEN_ADDRESS", "0.0.0.0")

r = IPResolver(answer_for=DNS_ANSWER_FOR)
logging.info(f"Listening on {DNS_LISTEN_ADDRESS}")

svr = DNSServer(r, port=DNS_LISTEN_PORT, address=DNS_LISTEN_ADDRESS)
tcp_svr = DNSServer(r, port=DNS_LISTEN_PORT, address=DNS_LISTEN_ADDRESS, tcp=True)
svr.start_thread()
tcp_svr.start_thread()
while svr.isAlive():
    time.sleep(0.2)
