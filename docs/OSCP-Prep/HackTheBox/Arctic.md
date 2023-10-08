# Arctic

## Recon  

The tags for [this box](https://app.hackthebox.com/machines/9) are:  
> - Windows
> - Arbitrary File Upload  
> - Patch Management
> - Web

Difficulty:
> Easy


### Port scan
There is a mystery service running on port 8500. The other open ports are RPC. Better figure out what the mystery service is.
```text
PORT      STATE SERVICE REASON          VERSION                                                                                                                              135/tcp   open  msrpc   syn-ack ttl 127 Microsoft Windows RPC                                                                                                                8500/tcp  open  fmtp?   syn-ack ttl 127                                                                                                                                      49154/tcp open  msrpc   syn-ack ttl 127 Microsoft Windows RPC                                                                                                                Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port                                                                        Device type: general purpose|phone|specialized                                                                                                                               Running (JUST GUESSING): Microsoft Windows 8|Phone|2008|7|8.1|Vista|2012 (92%) 
```

### Port 8500 - Cold Fusion 8
Software version disclosure
![[Pasted image 20220123055017.png]]

Searching for exploits
![[Pasted image 20220123055241.png]]

50057 looks promising. Interestingly enough, rhost and rport were already correct -it's almost like this exploit was developed/tested on this HTB box.
![[Pasted image 20220123060637.png]]

That gave us shell as `arctic\tolis`
![[Pasted image 20220123060841.png]]

User flag
![[Pasted image 20220123060946.png]]

## Privilege Escalation

### WinPEAS interesting findings
![[Pasted image 20220123093829.png]]


### Exploit Suggester
![[Pasted image 20220123145739.png]]

I've had luck with `MS10-059` in the past and figured that was a good way to go. I got the .exe from [SecWiki](https://github.com/SecWiki/windows-kernel-exploits/tree/master/MS10-059)

It worked, the listener (left) caught a system shell that was spawned by MS10-059 (right side).

![[Pasted image 20220123153545.png]]

Root flag:

![[Pasted image 20220123153626.png]]