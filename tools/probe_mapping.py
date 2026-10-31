"""Bounded comparison of STUN mappings; does not classify NAT filtering."""
import argparse
import json
from natter import StunClient

p = argparse.ArgumentParser()
p.add_argument('--source', required=True)
p.add_argument('--port', type=int, default=44380)
a = p.parse_args()
for udp in (False, True):
    servers = [('turn.cloudflare.com', 3478), ('global.turn.twilio.com', 3478)]
    if udp:
        servers += [('stun.miwifi.com', 3478), ('stun.chat.bilibili.com', 3478)]
    for server in servers:
        client = StunClient([server], a.source, a.port, udp=udp)
        try:
            inner, outer = client._get_mapping()
            result = {'protocol': 'udp' if udp else 'tcp', 'server': server,
                      'inner': inner, 'outer': outer}
        except Exception as exc:
            result = {'protocol': 'udp' if udp else 'tcp', 'server': server,
                      'error': str(exc)}
        print(json.dumps(result), flush=True)
