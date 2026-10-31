# Backup record

Date: 2026-10-31 (Asia/Shanghai).
Destination: `cidosc/hah-tools`, private, branch `main`.

## Scope and handling

Only the eight explicitly authorized source files below were copied into a
separate, freshly cloned empty repository. The original workspace was not edited.
The first commit contains those files, this record, a new safety README, an
allowlist-style .gitignore, and the matching third-party license text.
No previous workspace history is imported.

No source redaction was necessary. All eight copied files remain byte-identical
to their originals. Explicit-target helpers contain no historical machine address.
The remaining numeric literals are wildcard/loopback addresses, the standard SSDP
multicast address, an upstream public DNS default, and an upstream private-address
formatting example. Public STUN, keep-alive and
port-check service names belong to upstream/tool defaults, not private user assets.
The dated loopback response string is a fixed non-secret test label.

## Source manifest (SHA-256)

| Path | SHA-256 |
| --- | --- |
| `tools/loopback_probe_server.py` | `a5d892a413af360a76a1578e3ff139b40d400ba1c75b1d699d1f9c11cf9daf08` |
| `tools/prime_peers.py` | `4d0e28d80e5cb4843dad9f7783fca881c1c4461c96a5e09cec21df92101f9372` |
| `tools/probe_mapping.py` | `23004e6607f158418788067a23e7e7853288883f86926c70aa8625bf29dd385d` |
| `tools/review_network.py` | `156a59160bae2273ae9b875696ac495d586c423162132a7a875a8964f3927847` |
| `tools/vps_probe.py` | `2a9eb7da93e5cfbce1f19cf43f001c13b9189c1f52afff40ae1bdbb89d56391d` |
| `tools/natter.py` | `d384315dbb04413e17c5ddf3277b2f20466adc782ac020ff8dbed22165eec72a` |
| `tools/vendor/natter-check.py` | `8e6fdbad437714c4e55b88a06815fae220b78cad661473938981effc9b964dac` |
| `tools/vendor/README.md` | `e8adbf267ef5873e61f9c26c50a38e94f65dc2dbc448ae7f378825db0f201a55` |

## Third-party license evidence

- Upstream: https://github.com/MikeWang000000/Natter
- Source paths: `natter.py` and `natter-check/natter-check.py`; both declare
  Natter/NatterCheck v2.2.1 and copyright MikeWang000000 (2023).
- Both source headers expressly permit GNU GPL version 3 or any later version.
  The headers and no-warranty notices were retained.
- License source: https://github.com/MikeWang000000/Natter/blob/master/LICENSE
- Retrieved license Git blob: `e62ec04cdeece724caeeeeaeb6ae1f6af1bb6b9a`.
- License SHA-256: `605e9047a563c5c8396ffb18232aa4304ec56586aee537c45064c6fb425e44ad`.
- `LICENSES/Natter-GPL-3.0.txt` was compared byte-for-byte to the upstream
  license contents through a read-only GitHub API request. No third-party code
  was relicensed or represented as newly authored code.

## Explicit exclusions

Not copied, committed, or pushed:

- `inspection/`, H@H application/source archives, JARs and all downloaded ZIPs;
- `reports/`, packet captures, network test output and real IP inventories;
- access handoffs, real network architecture and deployment/status documents;
- private keys, SSH configuration, passwords, cookies, tokens and credential stores;
- databases, environment files, sessions, caches, bytecode and temporary helper files;
- GitHub Actions workflows, deployment services and automatic schedules.

The .gitignore excludes everything except the twelve named backup files. Files
were staged with an explicit filename list. Content checks and a first-history
review precede the initial push. No diagnostic program is executed as part of this
backup; offline content/AST inspection does not create sockets.

Two original third-party files have a terminal blank line. They are retained
byte-identically; the whitespace check ignores only blank-at-EOF for this reason.

## Remote verification

The existing GitHub connector and local GCM identity are `cidosc`. Verification
uses existing authentication only; no token is created, printed or saved into this
repository. Owner/privacy and Actions state are checked before and after the push.
Remote main must match the full local backup HEAD. No force push, permission
change, collaborator addition or deployment is part of this backup.
