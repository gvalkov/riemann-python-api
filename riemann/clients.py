#!/usr/bin/env python3
# -*- coding: utf-8; -*-

import ssl

import time
import socket
import logging
import threading

from . import transports
from . import riemann_pb2

log = logging.getLogger()
log.addHandler(logging.NullHandler())


class RiemannClient:
	def __init__(self, host='127.0.0.1', port=5555, timeout=None, transport=None):
		if transport:
			self.transport = transport
		else:
			self.transport = transports.TCPTransport(host, port, timeout)

	@classmethod
	def TCP(cls, host='localhost', port=5555, timeout=None):
		transport = transports.TCPTransport(host, port, timeout)
		return cls(transport)

	@classmethod
	def UDP(cls, host='localhost', port=5555):
		transport = transports.UDPTransport(host, port)
		return cls(transport)

	@classmethod
	def TLS(cls, host='localhost', port=5555, timeout=None,
			cert_reqs=ssl.CERT_REQUIRED, ca_certs=None):
		transport = transports.TLSTransport(host, port, timeout, cert_reqs, ca_certs)
		return cls(transport)

	def send(self, *events):
		msg = riemann_pb2.Msg()
		for event in events:
			if isinstance(event, dict):
				event = create_event(event)
			msg.events.add().MergeFrom(event)
		buf = msg.SerializeToString()
		res = self.transport.send(buf)
		return res

	def query(self, query):
		if isinstance(self.transport, transports.UDPTransport):
			raise Exception('querying over udp is not possible')

		msg = riemann_pb2.Msg()
		msg.query.string = query
		buf = msg.SerializeToString()
		res = self.transport.send(buf)

		return [parse_event(e) for e in res.events]


def parse_event(event):
	data = {}
	for descriptor, value in event.ListFields():
		if descriptor.name == 'tags':
			value = list(value)
		elif descriptor.name == 'attributes':
			value = {i.key: i.value for i in value}
		data[descriptor.name] = value

	return data


def create_event(data):
	event = riemann_pb2.Event()

	host = data.pop('host', socket.gethostname())
	tags = data.pop('tags', [])
	attr = data.pop('attributes', {})
	metric = data.pop('metric', None)

	event.host = host
	event.tags.extend(tags)

	if metric:
		autosize_metric_value(event, metric)

	for key, val in attr.items():
		at = event.attributes.add()
		at.key = key
		at.value = val

	for key, val in data.items():
		if val is not None:
			setattr(event, key, val)

	return event


def autosize_metric_value(event, value):
	if isinstance(value, int):
		if -(2**63) < value < 2**63:
			event.metric_sint64 = value
			event.metric_f = float(value)
	else:
		event.metric_d = value
		event.metric_f = value


__all__ = 'RiemannClient', 'parse_event', 'create_event'
