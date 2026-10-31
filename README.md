# hah-tools

Private source-only backup of a small, explicitly selected network-diagnostic toolkit.
This repository is an archive, not a deployment or an unattended diagnostic service.

## Contents

| File | Purpose |
| --- | --- |
| `tools/loopback_probe_server.py` | One fixed HTTP response on loopback; does not serve repository files |
| `tools/prime_peers.py` | Explicitly supplied source/peer SSH banner comparison |
| `tools/probe_mapping.py` | Explicit-source TCP/UDP STUN mapping comparison |
| `tools/review_network.py` | Gateway capability discovery and reference UDP classification |
| `tools/vps_probe.py` | Explicit-target TCP connect and bounded packet-header observation |
| `tools/natter.py` | Third-party Natter v2.2.1 source |
| `tools/vendor/natter-check.py` | Third-party NatterCheck v2.2.1 source |
| `tools/vendor/README.md` | Preserved third-party origin note |

Some scripts perform network I/O when invoked. Backing up this source does not run
them. No real host inventory, network findings, account material, or deployment
configuration is included. Supply only explicitly authorized targets when using
the tools separately.

Natter and NatterCheck retain their original MikeWang000000 copyright and
GPL-3.0-or-later notices. The matching upstream GPL version 3 license text is in
[`LICENSES/Natter-GPL-3.0.txt`](LICENSES/Natter-GPL-3.0.txt). This backup does not
claim authorship of third-party files or apply a new blanket license to the other
files. See [BACKUP.md](BACKUP.md) for scope, provenance, and exclusions.

There are no workflows or deployment files. GitHub Actions was confirmed disabled
before the initial push and is verified again after it.
