# Lame

## Recon

Tags for [this box](https://app.hackthebox.com/machines/1) are:  
> - injection
> - cms exploit

Difficulty:  
> Easy

### Port Scan
```
21/tcp   open  ftp         syn-ack ttl 63 vsftpd 2.3.4
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
22/tcp   open  ssh         syn-ack ttl 63 OpenSSH 4.7p1 Debian 
139/tcp  open  netbios-ssn syn-ack ttl 63 Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn syn-ack ttl 63 Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)
3632/tcp open  distccd     syn-ack ttl 63 distccd v1 ((GNU) 4.2.4 (Ubuntu 4.2.4-1ubuntu4))
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
OS fingerprint not ideal because: Missing a closed TCP port so results incomplete
Aggressive OS guesses: OpenWrt White Russian 0.9 (Linux 2.4.30) (92%), Linux 2.6.23 (92%)
```


## Exploitation
I decided to start with the odd service I hadn't seen before: **distcc**.

Hacktricks recommended checking if the metasploit module `exploit/unix/misc/distcc_exec` is applicable. Sure enough, I got a **daemon** account with this exploit. Thanks again HackTricks (all praise the xyz tld!)

![[190f47ced7744201bc8d99202531a032.png]]  
user `ebe6a4bdd37d05257c96607fb05b4486`

## Privilege Escalation

### Users
![[2019d3282e5a4b13a2c92f0de23f7ef0.png]]

### Listening ports
![[0f35a21db4be47449ade747c2d9ea1e6.png]]

### Local port scan
`nmap -sV -T5 127.0.0.1`
```
Starting Nmap 4.53 ( http://insecure.org ) at 2021-11-09 23:19 EST
who
Interesting ports on localhost (127.0.0.1):
Not shown: 1691 closed ports
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 2.3.4
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
23/tcp   open  telnet      Linux telnetd
25/tcp   open  smtp        Postfix smtpd
53/tcp   open  domain
80/tcp   open  http        Apache httpd 2.2.8 ((Ubuntu) DAV/2)
111/tcp  open  rpcbind      2 (rpc #100000)
139/tcp  open  netbios-ssn Samba smbd 3.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 3.X (workgroup: WORKGROUP)
512/tcp  open  exec?
513/tcp  open  rlogin
514/tcp  open  tcpwrapped
953/tcp  open  rndc?
1524/tcp open  ingreslock?
2049/tcp open  nfs          2-4 (rpc #100003)
2121/tcp open  ftp         ProFTPD 1.3.1
3306/tcp open  mysql       MySQL 5.0.51a-3ubuntu5
3632/tcp open  distccd     distccd v1 ((GNU) 4.2.4 (Ubuntu 4.2.4-1ubuntu4))
5432/tcp open  postgresql  PostgreSQL DB
5900/tcp open  vnc         VNC (protocol 3.3)
6000/tcp open  X11          (access denied)
6667/tcp open  irc         Unreal ircd
8009/tcp open  ajp13?
```

At this point I was stuck. I came back to this box later and was able to get root with the pictured metasploit module. Can't quite remember if I found this myself or looked into a write-up. Reminder to update this page if I find notes from this session.

![[Pasted image 20220103215557.png]]


## Reflect/Compare

In the official write-up for this box, everything was identical except the exploitation.
We both started with a full portscan, however I took a more arbirary route during exploitation; instead of working through the ports top-down, I just picked an interesting service I hadn't seen before.

My exploit:  
> Used `exploit/unix/misc/distcc_exec` metasploit modul  
> Which granted  user level access. I was unable to privesc  
> Later, I came back and used  `multi/samba/usermap_script`  
> Which granted root level access.  

HTB Writeup:
> Use `multi/samba/usermap_script`  
> Grants root level access  

### Analysis

While `distcc_exe` granted user level, it was a dead end as I couldn't figure out how to privesc. After this reflection, I'm confident that I 'found' the `usermap_script` exploit by looking at the writeup. This is a perfect example of **the dangers of immediately jumping to an exploit**.

Lessons Learned:

> DON'T just run around testing exploits. It wreckless and can lead to dead ends.  
> DO completely enumerate and try to weaponize each vector BEFORE thinking about exploitation.  

Exploitation should be closer to the end of my process. Put off exploitation attempts until I'm confident I have fully enumerated services/applications.