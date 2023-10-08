# Solidstate

`still in progress`

## Recon  

The tags for [this box](https://app.hackthebox.com/machines/85)  
> - File Misconfiguration
> - Web

Difficulty:
> Medium

### Port scan

```bash
PORT     STATE SERVICE REASON         VERSION                                                                                                                                22/tcp   open  ssh     syn-ack ttl 63 OpenSSH 7.4p1 Debian 10+deb9u1 (protocol 2.0)                                                                                                                                                                25/tcp   open  smtp    syn-ack ttl 63 JAMES smtpd 2.3.2                                                                                                                      |_smtp-commands: solidstate Hello nmap.scanme.org (10.10.16.3 [10.10.16.3])                                                                                                  80/tcp   open  http    syn-ack ttl 63 Apache httpd 2.4.25 ((Debian))                                                                                                         | http-methods:                                                                                                                                                              |_  Supported Methods: HEAD GET POST OPTIONS                                                                                                                                 |_http-title: Home - Solid State Security                                                                                                                                    |_http-server-header: Apache/2.4.25 (Debian)                                                                                                                                 110/tcp  open  pop3    syn-ack ttl 63 JAMES pop3d 2.3.2                                                                                                                      119/tcp  open  nntp    syn-ack ttl 63 JAMES nntpd (posting ok)                                                                                                               4555/tcp open  rsip?   syn-ack ttl 63       
```

## Services

The first thing I notice is JAMES. I've dealt with James in the OSCP lab and new what to look for.

### JAMES
There's a remote admin tool running on port 4555. The default credentials `root:root` allow you to list all users and change their passwords if desired. I did this and started digging through mail.

#### Users
![[Pasted image 20220123170932.png]]

#### Messages
Mindy's acct must be locked down, but also a password might be sitting in her email!

![[Pasted image 20220123171039.png]]

![[Pasted image 20220123171200.png]]

![[Pasted image 20220123171234.png]]

The ability to log in with Mindy's account, along with [EDB-50347](https://www.exploit-db.com/exploits/50347) will give us a normal shell as the user Mindy (as apposed to the `rbash` session that's her default.)

![[Pasted image 20220123171504.png]]

## Enumeration

### LinPEAS

![[Pasted image 20220123171542.png]]

![[Pasted image 20220123171552.png]]

![[Pasted image 20220123171608.png]]

