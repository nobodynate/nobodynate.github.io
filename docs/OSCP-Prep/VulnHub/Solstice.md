# Solstice

netdiscover found the VM runnin on this IP

```
192.168.1.191
```

## Service enumeration
### Pyftpdlib 1.5.6 ports 21 and 2121
tested anonymous (ftp:ftp) login - didn't work.

### Exim smtp 4.9.2
THis is running on port 25; we didn't find any valid accounts with `vrfy` wordlist attack.

### Squid httpd proxy 4.6
This is running on port 3128. We didn't see any webpages accessible from this port.

### http webservices
port 80, 8593, and 54787 have web services.

Port 80 has version disclosure on the homepage

![[Pasted image 20220708223833.png]]

on port 54787 `nikto` found the following page

```
http://192.168.1.191:54787/project/index.php
```

This is a login page, we were able to guess the credentials
username
```
admin
```
password
```
admin
```


at this point, we checked in with a walkthrough and it looks like we were possibly stuck in a rabbit hole

```
http://192.168.1.191:8593/index.php?book=
```
is vulnerable to LFI

We poisoned the logs with some php, then got a shell as www-data

we're able to see an interesting process running as root `/var/tmp/sv`

We modified the `index.php` page to contain a reverse shell then catch it with a netcat listener

## Root flag

![[Pasted image 20220709092008.png]]

