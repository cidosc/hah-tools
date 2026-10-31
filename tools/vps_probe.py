"""One outbound TCP connect plus bounded header-only packet observation."""
import select
import socket
import struct
import time
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('address', help='Current mapping IPv4 address, not a historical value')
parser.add_argument('port', type=int)
args = parser.parse_args()
socket.inet_pton(socket.AF_INET, args.address)
if not 1 <= args.port <= 65535:
    parser.error('port must be between 1 and 65535')
target = (args.address, args.port)
capture = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
capture.setblocking(False)
client = socket.socket()
client.setblocking(False)
started = time.monotonic()
print('connect_start', target, 'result', client.connect_ex(target), flush=True)
seen = 0
while time.monotonic() - started < 7:
    if not select.select([capture], [], [], 0.2)[0]:
        continue
    packet = capture.recv(128)
    if len(packet) < 54 or packet[12:14] != b'\x08\x00':
        continue
    ip = packet[14:]
    if ip[9] != 6:
        continue
    ihl = (ip[0] & 15) * 4
    if len(ip) < ihl + 20:
        continue
    src, dst = socket.inet_ntoa(ip[12:16]), socket.inet_ntoa(ip[16:20])
    sport, dport = struct.unpack('!HH', ip[ihl:ihl + 4])
    if (dst, dport) == target or (src, sport) == target:
        print('tcp_header', src, sport, '->', dst, dport,
              'flags', hex(ip[ihl + 13]), flush=True)
        seen += 1
ready = bool(select.select([], [client], [], 0)[1])
print('completed', ready, 'socket_error', client.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR),
      'matching_headers', seen, flush=True)
client.close()
capture.close()
