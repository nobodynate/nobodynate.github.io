# Blue

I knew this was going to use the Eternal Blue exploit, so I got Autoblue ready...however AutoBlue wasn't working. I was able to get this one working:

```
$ mkdir eternalblue 

$ curl https://raw.githubusercontent.com/helviojunior/MS17-010/master/send_and_execute.py > eternalblue/send_and_execute.py 

$ curl https://raw.githubusercontent.com/worawit/MS17-010/master/mysmb.py > eternalblue/mysmb.py 

$ curl https://raw.githubusercontent.com/worawit/MS17-010/master/checker.py > eternalblue/checker.py
```

this is saved in my `/opt/eternalblue` folder now.

Note, I was first getting a message about authentication failure, so I had to use the username `guest` in the scripts. Then everyhting worked well.

With this solution you need to provide an executable file (generate reverse shell with msfvenom)

# This uses python2

![[Pasted image 20220718150352.png]]