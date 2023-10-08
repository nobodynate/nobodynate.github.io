# Dawn
![[Pasted image 20220507133633.png]]

```bash
192.168.1.165
```

```bash
80/tcp   open  http        syn-ack ttl 64 Apache httpd 2.4.38 ((Debian))
139/tcp  open  netbios-ssn syn-ack ttl 64 Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn syn-ack ttl 64 Samba smbd 4.9.5-Debian (workgroup: WORKGROUP)
3306/tcp open  mysql       syn-ack ttl 64 MySQL 5.5.5-10.3.15-MariaDB-1
```

## 80 - webserver
Appears to be an internal IT Support site which is currently under construction

![[Pasted image 20220508084959.png]]

The `logs` directory on the webserver has some files.

I can only access `management.log`

![[Pasted image 20220508215501.png]]

It looks like there are 2 files being executed on some interval:

- `product-control` is being executed by UID: 1000

- `web-control` is b eing executed by UID: 33

![[Pasted image 20220508225848.png]]

## 139, 445 - SMB

I have Read/Write access to a share called ITDEPT. There is nothing on there but I'm able to upload stuff.

## 3306 - MySQL

There is a MariaDB server running which allows remote connections. The version is 5.5.5-10.3.15. There isa  plugin running called `mysql_native_password`. The plugin appears to be vulnerable but i haven't been able to exploit it yet. 

Then [answer from this page](https://dba.stackexchange.com/questions/209514/what-is-mysql-native-password) explains the plugin. And it can be exploited with [this POC](https://github.com/cyrus-and/mysql-unsha1).



# Exploitation
The SMB Share naem is the same as hte folder from logs. So I made a reverse shell named `product-control` and uploaded it to the webserver. After a few minutes I had a shell as the user Dawn.

Upgrade the shell
```python3
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

```bash
export TERM=xterm
```

## Enumerate Dawn

Lets take a look at Dawn's files

![[Pasted image 20220508220119.png]]

her bash history

![[Pasted image 20220508215954.png]]

her mysql history

![[Pasted image 20220508220055.png]]

# Linpeas findings
/bin/zsh has the SUID bit set.

I now have a root shell

![[Pasted image 20220508220942.png]]

Normally this is where I"ll stop, but I wasn't satisfied. There is a still a MySQL database full of info I didn't exfiltrate.

Tried hopping on the db as root:

![[Pasted image 20220508221643.png]]

So I need root's password. Maybe I can change it? It's dirty, but I can backup `/etc/shadow` before changing root's password then restore it to cover my tracks when I'm done

![[Pasted image 20220508221747.png]]

Hm...there was another user, maybe I can find something in their environment.

![[Pasted image 20220508221846.png]]


I ran
```bash
cat .bash_history
```

and violla! A password in cleartext!

![[Pasted image 20220508222018.png]]

```password
thisisareallysecurepasswordnooneisgoingtoeverfind
```

Now I'm able to get a proper root shell, AND explore the DB.

![[Pasted image 20220508222202.png]]

waiiiit....I still can't get into the DB.

Going to [reset the password](https://www.digitalocean.com/community/tutorials/how-to-reset-your-mysql-or-mariadb-root-password) so I can browse the DB to see what's in there.

And I'm in

![[Pasted image 20220508224028.png]]

Also, I was able to find the root password in `/root/.mysql_history`

![[Pasted image 20220508225024.png]]

There wasn't anything interesting in the database, as far as I can tell it was just a diversion. It worked, I spent way too much time trying to figure out how to exploit that dang mysql_naitive_password vulnerability, which ultimately I couldn't get to work.