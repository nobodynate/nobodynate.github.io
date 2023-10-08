# Noontide
## Enumeration

Netdiscover found the IP:

```
192.168.1.133
```

autorecon found 3 ports open:
- 6667
- 6697
- 8067

All 3 of these ports seem to be running `UnrealIRCd 3.2.8.1` and we were able to find a few exploits for this on searchsploit

![[Pasted image 20220710233054.png]]

We opted to use the metasploit module, and gained a shell as the user `server`

## User flag
![[Pasted image 20220710233158.png]]

we ran through some enumeration, noticed `sudo` is not available on this machine.
after exhausting all thinkable resources, we looked at a walkthrough, and found the username and password are `root:root` we just need to

```
su root
```

```
root
```

## Root flag

![[Pasted image 20220711000533.png]]