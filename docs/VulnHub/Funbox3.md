# Funbox3
![[Pasted image 20220511072612.png]]

```text
192.168.1.147
```


## Port Scan
```nmap
22/tcp    open  ssh     syn-ack ttl 64 OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp    open  http    syn-ack ttl 64 Apache httpd 2.4.41 ((Ubuntu))
33060/tcp open  socks5  syn-ack ttl 64

```


### Port 80: Apache webserver

default apache page is displayed at the root

![[Pasted image 20220511072643.png]]

robots.txt was disallowing `/gym`

#### /Gym

![[Pasted image 20220511072701.png]]

using LAMP not WAMP

![[Pasted image 20220511072743.png]]

#### CRM at /admin/

![[Pasted image 20220511073142.png]]

#### another CRM at /index.php

![[Pasted image 20220511073447.png]]

This one has username disclosure on the forgot password dialogue

![[Pasted image 20220511073543.png]]

There's also the option to register for this one

![[Pasted image 20220511073704.png]]

#### Bookstore at /store/

If this is projectworlds online bookstore 1.0, we could use [EDB-47887](https://www.exploit-db.com/exploits/47887)

![[Pasted image 20220511074012.png]]

Another login page

![[Pasted image 20220511074028.png]]

#### /secret/

![[Pasted image 20220511074221.png]]

## Foothold

I was able to get RCE as `www-data` with [EDB-47887](https://www.exploit-db.com/exploits/47887)

The shell was sort of shitty tho, so I replaced the payload with some php from `/usr/share/webshells/php/php-reverse-shell.php`

Then I had a fully interactive shell which allowed me to cd and such.

found `passwords.txt`

```text
ssh: yxcvbnmYYY
gym/admin: asdfghjklXXX
/store: admin@admin.com admin

```

I was able to log in as `tony` using the password he left me in his plaintext creds file.

Tony has some interesting sudoers entries

![[Pasted image 20220511080941.png]]

### Rooted

![[Pasted image 20220511081128.png]]

![[Pasted image 20220511081155.png]]