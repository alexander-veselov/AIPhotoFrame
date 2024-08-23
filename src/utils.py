import argparse

def valid_ip(address):
    try:
        parts = address.split('.')
        if len(parts) != 4:
            raise ValueError
        for part in parts:
            if not 0 <= int(part) <= 255:
                raise ValueError
        return address
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid IP address: '{address}'")

def valid_port(port):
    port = int(port)
    if not (0 <= port <= 65535):
        raise argparse.ArgumentTypeError(f"Invalid port number: '{port}'")
    return port