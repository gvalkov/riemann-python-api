#!/usr/bin/env python3
# -*- coding: utf-8; -*-

import ssl
import struct
import socket
import logging

from . import riemann_pb2

log = logging.getLogger()


class Transport:
    def __init__(self):
        self.connect()

    def __del__(self):
        self.disconnect()

    def send(self, message):
        pass


class SocketTransport(Transport):
    def disconnect(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()


class UDPTransport(SocketTransport):
    def __init__(self, host, port):
        self.address = (host, port)
        super().__init__()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, msg):
        self.socket.sendto(msg, self.address)


class TCPTransport(SocketTransport):
    def __init__(self, host, port, timeout):
        self.address = (host, port)
        self.timeout = timeout
        super().__init__()

    def connect(self):
        self.socket = socket.create_connection(self.address, self.timeout)

    def send(self, msg):
        buf = struct.pack('!I', len(msg)) + msg
        self.socket.sendall(buf)

        length = struct.unpack('!I', self.socket.recv(4))[0]
        res = riemann_pb2.Msg()
        res.ParseFromString(recvall(self.socket, length))
        return res


class TLSTransport(TCPTransport):
    def __init__(self, host, port, timeout, cert_reqs=ssl.CERT_REQUIRED, ca_certs=None):
        self.address = (host, port)
        self.timeout = timeout
        self.ca_cert = ca_certs
        self.cert_reqs = cert_reqs
        super().__init__(host, port, timeout)

    def connect(self):
        super().connect()
        self.socket = ssl.wrap_socket(
            self.socket,
            ssl_version=ssl.PROTOCOL_TLSv1,
            cert_reqs=self.cert_reqs,
            ca_certs=self.ca_certs
        )


class NullTransport(Transport):
    def __init__(self, *args, **kwargs):
        self.events = []
        super().__init__()

    def connect(self):
        pass

    def send(self, msg):
        for event in msg.events:
            self.events.append(event)
        reply = riemann_pb2.Msg()
        reply.ok = True
        return reply

    def disconnect(self):
        pass


def recvall(socket, length, bufsize=4096):
    data = b''
    while len(data) < length:
        data += socket.recv(bufsize)
    return data
