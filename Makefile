UPSTREAM_PROTO := https://raw.githubusercontent.com/riemann/riemann-java-client/master/riemann-java-client/src/main/proto/riemann/proto.proto

riemann.proto:
	curl -L $(UPSTREAM_PROTO) > $@

riemann/riemann_pb2.py: riemann.proto
	protoc $< --python_out=$(@D)

all: riemann/riemann_pb2.py
