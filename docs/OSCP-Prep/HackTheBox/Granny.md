# Granny
10.10.10.15

port 80 is open.

The website is under construction, but running IIS 6.0

Able to log in to WebDAV using cadaver with no credentials.

![[Pasted image 20220718094537.png]]

We're even able to upload files.

![[Pasted image 20220718094617.png]]

I am unable to upload `asp` files, they seem to be filtered, but we can add a `.txt` extension for upload then rename once it's up there.

I copied `/usr/share/webshells/aspx/cmdasp.aspx` to the webserver but it doesn't appear to work.

![[Pasted image 20220718102449.png]]

We see this is 32bit

![[Pasted image 20220718102621.png]]

We generate a reverse shell using `msfvenom` and upload the same way we did with the webshell.

We used `Windows-Exploit-Suggester` which found a few exploits, none which worked. Then we searched on google for `Windows Server 2003 privilege escallation` and found `Churrasco`.

Using `Churrasco` (MS09-012) we are able to run commands as system:

![[Pasted image 20220718114454.png]]

We copy over netcat and get a shell that way.

![[Pasted image 20220718114759.png]]

Now we can collect the user flag: `c:\documents and settings\lakis\desktop\user.txt` and the root flag `c:\documents and settigns\administrator\desktop\root.txt`

