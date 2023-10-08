Bloodhound

Get SPN for kerberoasting

timekeep webserver

password reset email

Malicious macro

get meterpreter

migrate to system

dump hashes

crack the new hash

enumerate teh db

# Task 29

cme to password spray

```bash
proxychains crackmapexec smb 10.200.70.117 -u <users> -p <passes>
```

# Task 30

Use bloodhound to `find principals with dcsync rights`

dump NTDS with impacket
```
secretsdump.py -dc-ip 10.200.70.117 Throwback/<user>@10.200.70.117
```

