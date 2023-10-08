# Skynet

## Recon

The room is terminator themed.

There is a user named **Miles** and we need to figure out his email password.

There is a hidden directory

File inclusion is mentioned.

## Port Scan

```bash
PORT    STATE SERVICE     REASON         VERSION
22/tcp  open  ssh         syn-ack ttl 61 OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http        syn-ack ttl 61 Apache httpd 2.4.18 ((Ubuntu))
110/tcp open  pop3        syn-ack ttl 61 Dovecot pop3d
139/tcp open  netbios-ssn syn-ack ttl 61 Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
143/tcp open  imap        syn-ack ttl 61 Dovecot imapd
445/tcp open  netbios-ssn syn-ack ttl 61 Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
Aggressive OS guesses: Linux 3.10 - 3.13 (95%), Linux 5.4 (95%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 3.16 (95%), Linux 3.1 (93%), Linux 3.2 (93%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (92%), Sony Android TV (Android 5.0) (92%), Android 5.0 - 6.0.1 (Linux 3.4) (92%), Android 5.1 (92%)
```

## Enumeration

### 22: OpenSSH 7.2p2

![[e2949122fe634797a45ae7e876dfd22c.png]]

### 80: Apache 2.4.18 - SquirrelMail 1.4.23

![[143f4f99178b4963acbca92be9744e32.png]]
![[c58a2943e7524dfc8ba2fce961f164fe.png]]
![[9d998321c54d4a788df3dc850adef1b6.png]]
![[cd81c2baefed41439d4206a33dcb7b5b.png]]
Each login attempt on Squirrel Mail takes 4+ seconds - not viable for a bruteforce.

### 110: Dovecot pop3d

![[407d9a6ef50b4299b8971cf7f17afbc4.png]]

### 139: Samba smbd 4.3.11-Ubuntu

![[c85f8503abcd4eefa18384284284d770.png]]
![[473b1d7f5fc64ef1a5565d3d1fef5156.png]]
![[603683708c07478a91d75c57442f3f13.png]]

### 143: Dovecot imapd

![[59fa321cc4ac45b6b4960ddce3a27570.png]]

### 445: Samba 4.3.11

![[4e889b70f42d4b6f907d3542859885ea.png]]

# Gaining access

Connected to **anonymous** Samba share on 139 using Anonymous
**Log1.txt** contains what appear to be passwords.
The first one listed is Miles' login for squirrelmail
**username**:`milesdyson`
**password**:`cyborg007haloterminator`

### Miles' SMB password is in email.

![[80f823697dbc4afeb68689b9d90fcd56.png]]

```
)s{A&2Z=F^n_E.B`
```

Connected to Miles' SMB share, in the folder **Notes** there is a file **important.txt** with contents:
![[9306cf5df0fc4cb388f075832770f1d1.png]]

```
/45kra24zxs28v3yd
```

another directory!
version 1.4.23 is vulnerable to RFI.

# Weaponization

Couldn't figure out what to do next.

Found there was an exploit for cuppa CMS - RFI and LFI

Turned to writeup to see that the next step was to use RFI on the Cuppa CMS page.

Got webshell

Moved to a reverse meterpreter (more compatible with privesc modules in metasploit

linux/local/ufo\_privilege\_escalation worked to get **root**

`3f0372db24753accc7179a282cd6a949`