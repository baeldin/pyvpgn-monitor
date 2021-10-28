import telnetlib

host = "127.0.0.1"
port = 8888
timeout = 100

session = telnetlib.Telnet(host, port, timeout)
session.write(b"tsuru110esr\n")
session.write(b"restart 900\n")
session.write(b"exit")