# Relevant

## Recon
### Flags:
- user.txt
- root.txt
### Rules: 
1. Manual exploitation preferred.
2. Locate/note all vulns found.
3. Submit flags to dashboard.
4. Stay in scope - stick to the room's box.
5. Find and report ALL vulnerabilities.

## nmap scan
```bash
└─$ nmap -sV -T5 10.10.89.145 | tee quickscan

Starting Nmap 7.92 ( https://nmap.org ) at 2021-11-04 21:29 CDT
Nmap scan report for 10.10.89.145
Host is up (0.21s latency).
Not shown: 995 filtered tcp ports (no-response)

PORT     STATE SERVICE            VERSION
80/tcp   open  http               Microsoft IIS httpd 10.0 (SSDP/UPnP)
135/tcp  open  msrpc              Microsoft Windows RPC
139/tcp  open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp open  ssl/ms-wbt-server?
49663/tcp open  http          syn-ack ttl 125 Microsoft IIS httpd 10.0                                            49667/tcp open  msrpc         syn-ack ttl 125 Microsoft Windows RPC                                               49669/tcp open  msrpc         syn-ack ttl 125 Microsoft Windows RPC

Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 100.75 seconds
```

# Service Enumeration
For the service enumeration, a more thorough scan was needed.
```bash
nmap -vv --reason -Pn -T4 -sV -sC --version-all -A --osscan-guess -p- -oN full_tcp_nmap.txt 10.10.89.145
```

## :80 - IIS 10.0
- X-Powered-By: ASP.NET
![[97db2002bf2d4664badd9fc29d1c0c31.png]]

## :135 - Microsoft Windows RPC
Many services exposed via RCP.
```text
Provider: appinfo.dll
Provider: BFE.DLL
Provider: certprop.dll
Provider: dhcpcsvc.dll
Provider: dhcpcsvc6.dll
Provider: gpsvc.dll
Provider: iphlpsvc.dll
Provider: MPSSVC.dll
Provider: msdtcprx.dll
Provider: N/A
Provider: nrpsrv.dll
Provider: nsisvc.dll
Provider: pcasvc.dll
Provider: samsrv.dll
Provider: schedsvc.dll
Provider: services.exe
Provider: spoolsv.exe
Provider: sppsvc.exe
Provider: srvsvc.dll
Provider: ssdpsrv.dll
Provider: sysntfy.dll
Provider: taskcomp.dll
Provider: wevtsvc.dll
Provider: wininit.exe
Provider: winlogon.exe
UUID    : FAF2447B-B348-4FEB-8DBE-BEEE5B7F7778 v1.0 OnlineProviderCert RPC Interface
Protocol: [MS-CMPO]: MSDTC Connection Manager:
Protocol: [MS-EVEN6]: EventLog Remoting Protocol
Protocol: [MS-PAN]: Print System Asynchronous Notification Protocol
Protocol: [MS-PAR]: Print System Asynchronous Remote Protocol
Protocol: [MS-RPRN]: Print System Remote Protocol
Protocol: [MS-RSP]: Remote Shutdown Protocol
Protocol: [MS-SAMR]: Security Account Manager (SAM) Remote Protocol
Protocol: [MS-SCMR]: Service Control Manager Remote Protocol
Protocol: [MS-TSCH]: Task Scheduler Service Remoting Protocol
```

## :139 - Microsoft Windows netbios-ssn
nothing worth noting.

## :445 - Windows Server 2016 Standard Evaluation 14393 microsoft-ds
Using **smb** the **Guest** can read **\\10.10.89.145\nt4wrksv\passwords.txt**
**passwords.txt**
`$ smbclient //10.10.67.66/nt4wrksv -U Guest`
Password is ` ` (nothing)
copied the files locally
`get passwords.txt`
![[ef63278930724f93a11a81f7e5da3a0d.png]]
Decode the password
```
$ echo "Qm9iIC0gIVBAJCRXMHJEITEyMw==" | base64 --decode
Bob - !P@$$W0rD!123 

$ echo "QmlsbCAtIEp1dzRubmFNNG40MjA2OTY5NjkhJCQk" | base64 --decode               
Bill - Juw4nnaM4n420696969!$$$
```

____
Username: 
```
Bob
```
Password: 
```
!P@$$W0rD!123
```

---
Username: 
```
Bill
```
Password: 
```
Juw4nnaM4n420696969!$$$
```

----
**Wonder what those credentials are for?**
Check these Vulnerabilities
![[39bb167de7544f2c81d97d85e8d9e727.png]]



## :3389 - Microsoft Terminal Services
Rdp, not much about it on there. Credentials didn't work with RDP.

## :49663 - IIS  10.0
 X-Powered-By: ASP.NET
 **page never loads in browser**

## OS Guess: 
### Windows Server 2008 R2
You're my boy Blue!
![[4e09aa57ce1b42c9a8823c49c7542bad.png]]
### Windows Server 2016 Standard Evaluation 14393 (Windows Server 2016 Standard Evaluation 6.3)

### Microsoft Windows Server 2016 (90%)

![[Pasted image 20220204224604.png]]




# Weaponization