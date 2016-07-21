import pytest


@pytest.fixture
def dummy_socket():
    return DummySocket()

class DummySocket:
    def __init__(self):
        self.data = [b'hello', b'world', b'']

    def recv(self, bufsize):
        return self.data.pop(0)

@pytest.fixture
def transport():
    return None
