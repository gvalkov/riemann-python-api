import pytest

from riemann import __main__ as main


@pytest.mark.parametrize('url,expected', [
    ['udp://127.0.0.1:2222', ('udp', '127.0.0.1', 2222)],
    ['tls://localhost:2222', ('tls', 'localhost', 2222)],
    ['test1.com',            ('tcp', 'test1.com', 5555)],
    ['test1.com:1111',       ('tcp', 'test1.com', 1111)],
])
def test_parse_connection_url(url, expected):
    assert main.parse_connection_url(url) == expected


@pytest.mark.parametrize('args,expected', [
    (['k1=v1', 'k2=v2'],    [{'k1': 'v1', 'k2': 'v2'}]),
    (['k1=v1', 'k2=a,b,c'], [{'k1': 'v1', 'k2': ['a', 'b', 'c']}]),

    (
        ['k1=v1', 'k2=v2', ';', 'k3=v3', 'k3=v3', ';', 'k4=v4'],
        [{'k1': 'v1', 'k2': 'v2'}, {'k3': 'v3', 'k3': 'v3'}, {'k4': 'v4'}]
    ),

    (['metric=1'],                  [{'metric': 1}]),
    (['metric=0.1'],                [{'metric': 0.1}]),
    (['metric_f=1', 'metric_d=2'],  [{'metric_f': 1.0, 'metric_d': 2.0}]),

])
def test_parse_insert_args(args, expected):
    assert main.parse_insert_args(args) == expected
