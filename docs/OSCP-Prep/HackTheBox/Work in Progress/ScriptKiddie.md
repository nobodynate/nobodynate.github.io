# Script Kiddie

`still in progress`

## Recon  

The tags for [this box](https://app.hackthebox.com/machines/314)  
> - Outdated software

Difficulty:
> Easy

### Port scan

Only 2 open ports on this one - 22 and 5000.

Port 22 has SSH running and port 5000 is a werkzug (python) webserver.

A recent piece of advice I heard is to enumerate the webserver last, because it's usually pretty complex and there's a lot of steps. So I checked for SSH exploits first. SSH doesn't really have a lot of useful exploits, and this version doesn't appear to have any public exploits.

On to the webserver!  
The webserver homepage has a few hacking tools on it. Nmap, searchsploit, and msfvenom. I tried doing command injection using the `;` and `&&` operators to string multiple commands together. But each tool seems to screen for that and display a message about "stop trying to hack me".  

The msfvenom tool is interesting. A user can upload an msfvenom template and then run an msfvenom command. Note: Some process on the server will be executing with data provided by the user.

I thought I was stuck so I started moving on but after taking these notes I think I should look closer at the msfvenom vector.