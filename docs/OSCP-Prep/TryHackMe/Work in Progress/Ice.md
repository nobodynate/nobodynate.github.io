# Ice

[This box](https://tryhackme.com/room/ice) is an introductory Windows box.

## Services

The tryhackme room is a walktrhough. We're focused on port 8000 which has `icecast` running.

## Vulnerability

[CVE-2004-1561](https://www.cvedetails.com/cve/CVE-2004-1561/ "CVE-2004-1561 security vulnerability details") provides code execution through buffer overflow.

Recommended to use metasploit. It was pretty simple and mostly worked as is.

`windows/http/icecast_header` is used as the initial foothold. Then we used exploit_suggester to find `windows/local/bypassuac_eventvwr`. The privesc exploit kept failing so I finally decided to migrate to an x64 system process (explorer.exe) and fire the exploit with x64 as the target. This gave me a successful privesc.

