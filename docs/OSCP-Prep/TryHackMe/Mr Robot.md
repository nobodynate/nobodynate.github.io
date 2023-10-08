# Mr. Robot

## Scanning
Ran nmap quick scan
``` bash
sudo nmap -sS -F -T5 10.10.31.9
```
![[f769f203af6e4d04b531d986fa985f27.png]]
Two ports are open (**80,443**) which are running webservers.
One port is closed (**22**) which is running ssh.

## Webserver on 80
The front end is similar to a flash video game. You can enter different commands which each display some content.
I examined the startup video closely, there don't appear to be any flags in there.

### Robots.txt
![[99d012eb852444f2b71695033f5e0465.png]]
Get each Robots.txt page
![[b5c5915a322a45ab837f14064b7aae3b.png]]
**key-1-of-3.txt**
``` bash
073403c8a58a1f80d943455fb30724b9
```

# Hint 2
![[ab67eac23ee6409593a9bff4a5212928.png]]
I quickly examined the startup video...nothing there.
From checking CSS it appears there's a footer with white text that appears when you hover it.

# WordPress - Version 4.3.1
## Theme twentyfifteen