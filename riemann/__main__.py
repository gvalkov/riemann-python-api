import os
import sys
import optparse

from . import clients
from . import transports


USAGE = '''\
Usage: %(prog)s [options] [<url>] <insert|query> <script>

Tool for quering or sending events to Riemann. Example usage:

  %(prog)s tcp://127.0.0.1:5555 insert service=B tags=a,b,c metric=100
  %(prog)s udp://127.0.0.1:5555 insert "{'service': 'B', 'metric': 100}"

Connection string:
  Specifying the location of the Riemann server can be done with the first
  positional argument. The accepted format is scheme://host:port, where scheme
  and port are optional and default to 'tcp' and '5555'. The available
  connection schemes are: tcp udp tls

  If the connection string is omitted, the tool will attempt to connect to
  'tcp://localhost:5555' or the value of the RIEMANN_TOOL_URL environment
  variable.

Inserting events:
  This tool supports several formats for inserting events into Riemann.

  Single event:
    insert service=example metric=1 tags=A,B

  Single event (dictionary syntax):
    insert "{'service': 'example', 'metric': 1, 'tags': ['A', 'B']}"

  Multiple events (note the escaped ; (semicolon) character):
    insert service=ex1 metric=1 \; service=ex2 metric=2

  Multiple events (dictionary syntax):
    insert "{'key': 'value'}" "{'key': 'value'}"

  Reading events from stdin:
    %(prog)s insert - <<<EOF
    {'key': 'value'}
    {'key': 'value'}
    EOF

Querying events:
  query true

Options:
  -t, --timeout <sec>   TCP connection timeout

'''


scheme_transport = {
	'tcp': transports.TCPTransport,
	'udp': transports.UDPTransport,
	'tls': transports.TLSTransport,
}


def parse_connection_url(uri, default_scheme='tcp', default_port=5555):
	scheme, sep, rest = uri.partition('://')
	if not sep:
		rest = scheme
		scheme = default_scheme

	host, sep, port = rest.rpartition(':')
	if not sep:
		host = port
		port = default_port

	return scheme, host, int(port)


def parseargs(args):
	parser = optparse.OptionParser(prog='python -m riemann', add_help_option=False)
	parser.add_option('-t', '--timeout')
	opts, args = parser.parse_args()

	usage = USAGE.rstrip() % {'prog': 'python -m riemann'}

	if not args:
		print(usage, file=sys.stderr)
		sys.exit(2)

	if args[0] in {'insert', 'query'}:
		default_url = os.environ.get('RIEMANN_TOOL_URL', 'tcp://localhost:5555')
		scheme, host, port = parse_connection_url(default_url)
	else:
		scheme, host, port = parse_connection_url(args[0])
		args.pop(0)

	transport = scheme_transport[scheme](host, port, opts.timeout)
	client = clients.RiemannClient(transport=transport)

	if not args:
		print(usage, file=sys.stderr)
		print('\nerror: missing command', file=sys.stderr)
		sys.exit(2)

	if args[0] == 'insert':
		cmd_insert(client, args[1:])
	elif args[0] == 'query':
		cmd_query(client, args[:1])
	else:
		print('\nerror: unknown command: %s' % args[0], file=sys.stderr)
		sys.exit(2)


class InsertArgsParser:
	def __call__(self, args):
		if '=' in args[0]:
			return self.parse_key_value(args)
		if args[0].startswith('{'):
			return self.parse_dict(args)

	@staticmethod
	def float_or_int(s):
		try:
			f = float(s)
			if f.is_integer():
				return int(s)
			return f
		except ValueError:
			return s

	def parse_key_value(self, args):
		args = args[:]
		if args[-1] != ';':
			args.append(';')

		events = []

		event = {}
		for arg in args:
			if arg == ';':
				events.append(event)
				event = {}
				continue
			key, value = arg.split('=', 1)

			if key == 'metric':
				value = self.float_or_int(value)
			elif key in {'metric_f', 'metric_d'}:
				value = float(value)
			elif ',' in value:
				value = value.split(',')

			event[key] = value
		return events

parse_insert_args = InsertArgsParser()

def cmd_insert(client, args):
	events = parse_insert_args(args)
	client.send(*events)

def cmd_query(client, args):
	pass


def main(args=sys.argv):
	args = parseargs(sys.argv)


if __name__ == '__main__':
	main()
