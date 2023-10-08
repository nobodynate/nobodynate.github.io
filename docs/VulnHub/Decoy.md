# Decoy

Netdiscover found this one running on

```
192.168.1.170
```

port scan reveals port 80 and 22

on port 80 we find a webserver which has a password protected zip file

![[Pasted image 20220710220811.png]]

we used `zip2john` and `john` to crack the password

```
server           (296640a3b825115a47b68fc44501c828)
```

we can ssh as the user `296640a3b825115a47b68fc44501c828` with password `server` however this is a very limited `rbash` session.

After poking around I noticed the PATH is set to my home directory, so I used `scp` to copy over `/bin/sh` from my kali machine and was able to break out of rbash using that

```
sh
```

now we fix the path

```
PATH=PATH$:/usr/local/sbin:/usr/local/bin:/usr/sbin:/sbin:/bin;export PATH
```

at this point we ended up looking at a walkthrough. There was a binary file in our home directory which gave us access to `chkrootkit 0.49` [EDB-33899](https://www.exploit-db.com/exploits/33899)

We are able to verify the software and version by looking through logs in the `SV-502` logs.

## Root flag
![[Pasted image 20220710225740.png]]