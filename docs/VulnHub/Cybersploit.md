# Cybersploit
# Port scan
```bash
22/tcp open  ssh     syn-ack ttl 64 OpenSSH 5.9p1 Debian 5ubuntu1.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 64 Apache httpd 2.2.22 ((Ubuntu))
```

## Port 80
Homepage, none of the nav buttons appear to do anything.
![[Pasted image 20220507080101.png]]

Found a username `itsskv` in the HTML comments
![[Pasted image 20220507080133.png]]

Robots.txt has a long string
![[Pasted image 20220507080218.png]]

Long string base64 decoded: 
![[Pasted image 20220507080315.png]]

```
Good Work !
Flag1: cybersploit{youtube.com/c/cybersploit}
```

Now have some secret data and a username, tried logging in: 

```bash
ssh itsskv@192.168.1.114
```

Password: `cybersploit{youtube.com/c/cybersploit}`

It worked

![[Pasted image 20220507142551.png]]

found another flag
![[Pasted image 20220507143030.png]]


![[Pasted image 20220507143013.png]]

`cybersploit{https:t.me/cybersploit1}`

I tried to su to cybersploit user and to root using this flag as the password. That did not work.

I ran linpeas and didn't see any config issues.

The only thing that really stands out is the old linux version. Linux-exploit-suggester recommends `dirtycow`(fail),`dirtycow2`(fail), `overlay-fs`(pass)

# Privesc with overlayfs
Using [edb-37292](https://www.exploit-db.com/download/37292) (CVE-2015-1328) I was able to get a root shell.

![[Pasted image 20220507150323.png]]

![[Pasted image 20220507150414.png]]

`cybersploit{Z3X21CW42C4 many many congratulations !}`