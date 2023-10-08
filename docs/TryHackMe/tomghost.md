# Tomghost

## Recon
Based on the name it appears to be **Apache Tomcat** related.
The **username** contains a swear word.

# Scanning
```
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
53/tcp   open  tcpwrapped
8009/tcp open  ajp13      Apache Jserv (Protocol v1.3)
8080/tcp open  http       Apache Tomcat 9.0.30
```

# Enumerating external services
## 8080 - Apache Tomcat 9.0.30, default configuration
![[cb107eef217c4d25ba2f329c17839004]]

# Weaponization
This looks promising given the circumstances.
![[10dfa5e248f3439bba1150544d1d0149]]
Loot from that exploit
![[66fce28faa1043f5a01f2fba965268ba]]
user: `skyfuck`
pass: `8730281lkjlkjdqlksalks`

Those creds worked for **SSH**
![[5df9e7ae0e2c4e82b92609bd3220a250]]
users
![[95c5c24ce16f4928a6e563df06b98df9]]
User flag `THM{GhostCat_1s_so_cr4sy}`
![[147b615eed7d42feab2a814435a76cae]]

Upload and run linpeas
![[c34aeb9fcb1845d6a4cce59b28c35361]]

Found an SSH private key?
![[08acb0f4a1ae422b81263a5e657455ff]]
![[82cbdc81dcd34819a8653bd738a082d9]]

Looks like we need to log in as root using the private key.

Port 8005 is only available from the inside.
![[e7cf94e7cca04d3b8289abb5f54235e8]]

Not sure what this is
![[3f1ed64670824d8aa4275cbd7ffebd39]]

## Going to try cracking the passphrase for PGP private key.
First send it through gpg2john
![[041666ac7efa49c4a9cff0444ac8b092]]
Then use john to crack
![[e7a72984499946b5bb8a44b715abe55a]]

Cracked in record time when I switched to rockyou.txt!
![[001f34ebb80b4cd9823f2befcdaca6ae]]

file: `tryhackme`
pass: `alexandru`
### Import the pgp key
![[968a427301084bd686b8523918aa82ac]]
### Decrypt the credential
![[2c47147ea5ca456f8db2481192da7253]]

Logged in as merlin, I have sudo privs for zip.
GTFObins gave me root shell
https://gtfobins.github.io/gtfobins/zip/
![[6aee0a72ac87482b836f2bae68b22254]]