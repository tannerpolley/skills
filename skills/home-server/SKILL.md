---
name: home-server
description: Run, deploy, check, restart, turn on or off, or remove long-running servers (web apps, game servers, Home Assistant, sync hubs, bots, anything that must stay up) on the always-on Chromebox reached by `ssh chromebox`.
---

# Home server (Chromebox)

The user's always-on Chromebox hosts their servers. They want agents to use it freely: anything that should keep running after this session ends belongs there as a systemd service (or a libvirt VM), not on the Linux PC and not in an SSH session.

## Facts

| What | Value |
|---|---|
| Reach | `ssh chromebox` from the Linux PC: user `tanner` with passwordless `sudo`, OpenSSH with a key, over Tailscale. |
| Addresses | Tailscale `chromebox.taila72856.ts.net` / `100.72.81.99`. Wired LAN on bridge `br0` (DHCP, around `10.0.0.48`). |
| Machine | Acer Chromebox CXI3: Celeron 3865U (2 cores), **~3.3 GB RAM** (one 8 GB stick planned), 27 GB disk. Memory and disk are the limits. |
| OS | Ubuntu Server 26.04 LTS with automatic security updates. Python 3.14, .NET 10 runtime, KVM/libvirt, Syncthing v2 (official repo). |
| Layout | Each server's files live in `/srv/<name>/`, owned by the non-login system user `srv`. Secrets go in `/etc/home-server/<name>.env` (root, mode 600) through `EnvironmentFile=`. |
| Registry | A server is `/etc/systemd/system/<name>.service` whose `Description=` starts with `<name> (home server): ` and says where its source lives, or a libvirt VM. `server list` reads exactly this. |
| On/off | On the Linux PC: `server list`, `server on|off|restart|status|logs <name>`, `server boot-on|boot-off <name>` (`~/.local/bin/server`). For the user: Cockpit at https://chromebox.taila72856.ts.net:8443 (log in as `tanner`). |

Current servers (game servers are owned by their folders in `~/Workspaces/Games/`; Terraria left the Chromebox on 2026-10-26 and its unit there is disabled; Forgejo moved to the Linux PC on 2026-11-02 as the system service `forgejo` at https://tnnrpolley21-ms-7c95.taila72856.ts.net:3000, data in `/srv/forgejo`, admin `tannerpolley` with the password in `~/.config/home-server/forgejo-admin-password`): `recipes` (https://chromebox.taila72856.ts.net), `syncthing-hub` (emulator saves; GUI through `ssh -L 8384:127.0.0.1:8384 chromebox`), and the VM `home-assistant` (http://10.0.0.170:8123; paused, see the plan notes before starting it).

## Add or update a server

1. **Budget**: check `free -m` and `df -h /` on the Chromebox. If the new server would leave under ~500 MB of memory or ~2 GB of disk, ask the user before installing it.
2. **Stage files** in `/srv/<name>/` and `chown -R srv:srv` them. Build on the Linux PC when the Chromebox lacks the toolchain, then copy the output (`tar ... | ssh chromebox 'sudo tar -C /srv/<name> -xf -'`). Generate secret files on the PC without echoing them.
3. **Write the unit** by copying the closest existing one: `recipes.service` for a plain process, `terraria.service` for a server that saves on Ctrl+C. Keep `User=srv`, `Restart=on-failure`, `WantedBy=multi-user.target`, and the Description convention. Then `sudo systemctl daemon-reload && sudo systemctl enable --now <name>`.
4. **Expose** only as far as needed:
   - **Tailnet and home LAN**: automatic. No host firewall is enabled, so a server bound to `0.0.0.0` is reachable from both.
   - **HTTPS name**: `sudo tailscale serve --bg --https=<port> http://127.0.0.1:<port>` (443 is `recipes`, 8443 is Cockpit).
   - **Public internet** (router port forward or Tailscale Funnel): ask the user first.
5. **Verify** from the Linux PC: `server list` shows it active, the port answers over the tailnet, `server logs <name>` shows a clean start, and `server off` then `server on` works.

## Remove a server

`sudo systemctl disable --now <name>`, then delete its unit, `/srv/<name>`, `/etc/home-server/<name>.env`, and any `tailscale serve` mapping.

## Gotchas

- A server that saves on Ctrl+C: set `KillSignal=SIGINT` and `TimeoutStopSec=`. If anything else runs in its control group (such as a helper process), add `KillMode=mixed`, so only the server gets the signal and the rest are killed once it exits.
- A console server must never see end of input on stdin, or it spins at high CPU. `terraria.service` keeps stdin open with `< <(exec sleep infinity)`.
- Single-file .NET apps unpack themselves on first run. Give them `CacheDirectory=<name>` and `Environment=DOTNET_BUNDLE_EXTRACT_BASE_DIR=/var/cache/<name>`, since `srv` can't write its home.
- VMs: `virsh -c qemu:///system`, disks in `/var/lib/libvirt/images`, bridged on `br0`. `libvirt-guests` presses each VM's power button at host shutdown and waits up to 120 s; `virsh autostart` starts them at boot.
- A bind to `127.0.0.1` stays private to the Chromebox. Some apps, `recipes` among them, switch to an unauthenticated local mode when bound there, so check how an app treats localhost before putting `tailscale serve` in front of it.
