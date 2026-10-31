"""Bounded capability discovery. Never sends a gateway mapping request.

Run under an outer timeout (e.g. timeout 70s) because DNS is OS-dependent.
NAT-PMP opcode 0 and PCP ANNOUNCE only query gateway capabilities.
"""
import argparse
import datetime
import ipaddress
import json
from pathlib import Path
import runpy
import socket
import struct
import time

from natter import StunClient


def emit(kind, **values):
    print(json.dumps({'time_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      'kind': kind, **values}), flush=True)


def gateway_query(source, gateway, protocol):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((source, 0))
        sock.settimeout(2)
        sock.connect((gateway, 5351))
        if protocol == 'nat-pmp':
            request = b'\x00\x00'  # Public-address query, NOT a port mapping.
        else:
            client_ip = ipaddress.IPv6Address('::ffff:' + source).packed
            request = struct.pack('!BBHI', 2, 0, 0, 0) + client_ip
        try:
            sock.send(request)
            data = sock.recv(128)
            if protocol == 'nat-pmp' and len(data) >= 12 and data[:2] == b'\x00\x80':
                emit(protocol, result=struct.unpack('!H', data[2:4])[0],
                     reported_address=socket.inet_ntoa(data[8:12]))
            elif protocol == 'pcp' and len(data) >= 24 and data[:2] == b'\x02\x80':
                emit(protocol, result=data[3])
            else:
                emit(protocol, result='unexpected_response', length=len(data))
        except OSError as exc:
            emit(protocol, result='no_valid_response', detail=str(exc))


def discover_igd(source):
    found = set()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((source, 0))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(source))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        request = ('M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\n'
                   'MAN: "ssdp:discover"\r\nMX: 1\r\n'
                   'ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n\r\n')
        sock.sendto(request.encode('ascii'), ('239.255.255.250', 1900))
        deadline = time.monotonic() + 3
        while len(found) < 8 and time.monotonic() < deadline:
            sock.settimeout(max(0.01, deadline - time.monotonic()))
            try:
                data, peer = sock.recvfrom(4096)
                if data.startswith(b'HTTP/1.1 200'):
                    found.add(peer[0])
            except socket.timeout:
                break
    emit('upnp_igd_discovery', responder_addresses=sorted(found), mappings_requested=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=ipaddress.IPv4Address, required=True)
    parser.add_argument('--gateway', type=ipaddress.IPv4Address, required=True)
    parser.add_argument('--port', type=int, default=44386)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error('port must be between 1 and 65535')
    vendor = Path(__file__).parent / 'vendor' / 'natter-check.py'
    if not vendor.is_file():
        parser.error('copy tools/vendor/natter-check.py before running this review')
    source, gateway = str(args.source), str(args.gateway)
    for protocol in ['nat-pmp', 'pcp']:
        gateway_query(source, gateway, protocol)
    discover_igd(source)
    for host in ['turn.cloudflare.com', 'global.turn.twilio.com']:
        try:
            inner, outer = StunClient([(host, 3478)], source, args.port)._get_mapping()
            emit('tcp_mapping_only', server=host, inner=inner, outer=outer)
        except Exception as exc:
            emit('tcp_mapping_only', server=host, error=str(exc))
    cls = runpy.run_path(str(vendor), run_name='natter_check_library')['StunTest']
    cls.stun_server_tcp = ['turn.cloudflare.com', 'global.turn.twilio.com']
    cls.stun_server_udp = ['stun.miwifi.com', 'stun.chat.bilibili.com']
    check = cls(source_ip=source)
    emit('udp_behavior_start')
    nat_type = check.check_udp_nat_type(source_port=args.port)
    names = {-1: 'unknown', 0: 'open_internet', 1: 'full_cone', 2: 'restricted_cone',
             3: 'port_restricted_cone', 4: 'symmetric', 5: 'symmetric_udp_firewall'}
    emit('udp_behavior', nat_type=nat_type, name=names.get(nat_type, 'unknown'),
         limitation='UDP only, public STUN service behavior can affect classification')


if __name__ == '__main__':
    main()
