# Grandpa

10.10.10.14

This box only has port 80 open. It's running IIS 6.0. We find this service is vulnerable to CVE-2017-7296. We found an exploit script [here](https://github.com/g0rx/iis6-exploit-2017-CVE-2017-7269)

This gives us a shell as NETWORK SERVICE and we immediately notice we have SEIMPERSONATE priv enabled.

I tried a few exploits but nothing seemed to work. Eventually I turned to a walkthrough and found the correct way to exploit Windows Server 2003 SP2 with SEImpersonate is to use [Churrasco](https://github.com/Re4son/Churrasco)

This gives us a shell as SYSTEM. We find the flags

`c:\Documents and Settings\harry\Desktop\user.txt` and
`c:\Documents and Settings\Administrator\Desktop\root.txt`

