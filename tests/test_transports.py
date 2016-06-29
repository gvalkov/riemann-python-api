import pytest

from riemann import transports


def test_socket_recvall_1(dummy_socket):
	assert transports.recvall(dummy_socket, 10) == b'helloworld'

def test_socket_recvall_2(dummy_socket):
	assert transports.recvall(dummy_socket, 10) == b'helloworld'
