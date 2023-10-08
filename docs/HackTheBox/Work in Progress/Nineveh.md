# Nineveh

`still in progress`
## Recon

Tags for [this box](https://app.hackthebox.com/machines/54):  
> - LFI
> - Web 
> - PHP
> - Port knocking

Difficulty:
> Medium


### Port scan
```text
PORT    STATE SERVICE  REASON         VERSION
80/tcp  open  http     syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
| http-methods:
|_  Supported Methods: POST OPTIONS GET HEAD
|_http-server-header: Apache/2.4.18 (Ubuntu)
443/tcp open  ssl/http syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
| http-methods:
|_  Supported Methods: POST OPTIONS GET HEAD
```

Nikto identified RFI
> + OSVDB-5292: /info.php?file=http://cirt.net/rfiinc.txt?: RFI from RSnake's list (http://ha.ckers.org/weird/rfi-locations.dat) or from http://osvdb.org/

I did a POC by hosting "Hello Wolrd" in a text file and trying to load it. The string doesn't appear anywhere on the info page. It seems like this exploit won't work on this box.


