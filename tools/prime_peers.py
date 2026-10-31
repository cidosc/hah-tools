"""Brief SSH banner-only connects from the mapped port; no authentication."""
import select
import socket
import argparse
from natter import socket_set_opt, StunClient

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', required=True, help='Current local campus IPv4')
parser.add_argument('--port', type=int, required=True, help='Current Natter local port')
parser.add_argument('--peer', action='append', required=True, help='Authorized VPS IPv4; repeat for each peer')
args = parser.parse_args()
socket.inet_pton(socket.AF_INET, args.source)
for peer in args.peer:
    socket.inet_pton(socket.AF_INET, peer)
if not 1 <= args.port <= 65535:
    parser.error('port must be between 1 and 65535')
held = []
for host in args.peer:
    sock = socket.socket()
    socket_set_opt(sock, reuse=True, bind_addr=(args.source, args.port), timeout=4)
    try:
        sock.connect((host, 22))
        print('outbound_connected', host, 'banner', sock.recv(100).decode(errors='replace').strip(), flush=True)
        held.append(sock)
    except OSError as exc:
        print('outbound_failed', host, str(exc), flush=True)
        sock.close()
try:
    print('mapping_after_outbound', StunClient([('turn.cloudflare.com', 3478)], args.source, args.port)._get_mapping(), flush=True)
except Exception as exc:
    print('mapping_error', str(exc), flush=True)
select.select([], [], [], 40)
for sock in held:
    sock.close()
