# Vegeta

netdiscover finds this IP

```
192.168.1.113
```

autorecon finds port 22 and port 80.

we found an entry in `robots.txt` and followed it

![[Pasted image 20220711003025.png]]

![[Pasted image 20220711003043.png]]

![[Pasted image 20220711003057.png]]

This brings us to a page with some encoded string in an HTML comment. We couldn't decode this to anything useful.

Looked at a walkthrough, which finds `/bulba/`

There is a .wav file which has a morse code encoded message.

```
trunks
```

```
u$3r
```

we should be able to log in with

```
ssh trunks@192.168.1.113
```

we are owner of the `/etc/passwd` file and if we look at the `history` we see a command that adds a new user `Tom` with root permissions. We run the command, and log into Tom's account with

```
su Tom
```

## Root flag

![[Pasted image 20220711004029.png]]

