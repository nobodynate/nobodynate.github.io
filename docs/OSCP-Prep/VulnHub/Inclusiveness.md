# Inclusiveness

## Port scan
```bash
21/tcp open  ftp     syn-ack ttl 64 vsftpd 3.0.3
22/tcp open  ssh     syn-ack ttl 64 OpenSSH 7.9p1 Debian 10+deb10u1 (protocol 2.0)
80/tcp open  http    syn-ack ttl 64 Apache httpd 2.4.38 ((Debian))
```

Ftp allows anonymous login

Dirbuster found `robots.txt` on port 80 but it is not allowing me to read view the content.

There is a hint

![[Pasted image 20220528110607.png]]

I was able to bypass the restriction by forcing the User-Agent to be `Googlebot`

![[Pasted image 20220528110720.png]]

Now we can see the content of robots.txt

![[Pasted image 20220528110754.png]]

The `/secret_information/` page has a few links that add a `lang` parameter to the URL.

This parameter is vulnerable to LFI

![[Pasted image 20220528111415.png]]

I am able to upload to the ftp in `/pub/` which has a path of `/var/ftp/pub/` on the linux server.

![[Pasted image 20220528120015.png]]

Now do the same with a reverse php shell.

This gives a shell as www-data

![[Pasted image 20220528120229.png]]

upgrade the shell

```python3
python -c 'import pty; pty.spawn("/bin/bash")'
```

```bash
export TERM=xterm
```


Found an interesting binary with SUID set `/home/tom/rootshell`.

Reviewing the code it looks like I can get root if it thinks I'm tom. I just need to spoof the whois command.

Fake `whois` with path injeciton.

```bash
echo "printf 'tom'"" > /tmp/whoami
```

Add /tmp to the path
```bash
export PATH=/tmp:$PATH
```

execute the SUID binary
```bash
/home/tom/rootshell
```

Now I have a shell as tom.

![[Pasted image 20220528202006.png]]

Tom can sudo everything with no password, so becoming root is as easy as `sudo su`

![[Pasted image 20220528202031.png]]

I am root

![[Pasted image 20220528202103.png]]

