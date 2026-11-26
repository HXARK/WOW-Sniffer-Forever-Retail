# HXARK Sniffer

WoW Retail and Forever packet capture for Windows. Saves PKT files automatically.

[Discord](https://discord.gg/P9RWZQBQkZ) · [Downloads](https://github.com/HXARK/WOW-Sniffer-Forever-Retail/releases/latest)

Windows x64, IPv4. Latest validated builds:

- **Retail 12.1.5 — 70961**
- **Forever 1.60.1 — 71139**

## Use

1. Open the sniffer and wait for **Ready**.
2. Open WoW, log in and play.
3. Close WoW. Click **Open captures** to find the saved PKTs.

On first use, select `Wow.exe` if requested. Use **Install capture support** if
needed and keep **Npcap** selected in the Wireshark installer. Wireshark does not
need to stay open.

Retail and Forever are detected in the same Battle.net installation folder.
Open one game client at a time. You can leave the sniffer open between sessions.

## Captures

Use **Change folder** before opening WoW to choose where files are saved.
Each session has its own folder under `dumps`. A session can produce several PKTs.
Retail filenames include locations when recognized; Forever filenames use the
build and timestamp.

The default folder is `%LOCALAPPDATA%\HXARK\Sniffer`. Recovery data stays under
`captures`. Keep captures and recovery files private. Nothing is uploaded.

PKTs include timestamps, UTC offset, game locale and connection identifiers.
The adjacent `.pkt.capture.json` records the checksum, counts and capture status.
Interrupted captures and reported packet loss are flagged in the app.

## Parsing

Parse PKTs separately with a parser that supports the captured build, such as
[TrinityCore WowPacketParser](https://github.com/TrinityCore/WowPacketParser).
The sniffer does not include a parser.

## Updates and limits

New WoW builds need validation. Download the updated EXE when support is added.

Capture limits: 12 hours, 1 GiB input, 1 million candidate packets, 8 interfaces,
32 flows per interface and 32 session-key snapshots. The app warns near these
limits and keeps recovery data if capture stops early. IPv6 is not captured.

## Build

Windows x64, Python 3.14 with Tcl/Tk:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe scripts/build_sniffer_staff.py
```

Output: EXE, SHA-256 and build manifest in `dist`. To run from source:

```powershell
.\.venv\Scripts\python.exe scripts/sniffer_staff.py
```

## License

[MIT](LICENSE). Third-party notices: [NOTICE](NOTICE).
EXEs are not Authenticode signed. Use only on sessions you are authorized to capture.

By [HXARK](https://hxark.com). Not affiliated with Blizzard, Wireshark or Npcap.
