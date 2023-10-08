
We found the IP using `netdiscover`
```text
192.168.1.149
```

A port scan reveals port 80 is running a webserver.
We see Nagios XI running on this webserver

![[Pasted image 20220627120510.png]]

We found a few public exploits for Nagios XI, some of which appear to require credentials.

We tested EDB-44560 and EDB-49422 but neither seemed to work.

Using the metasploit module `linux/http/nagios_xi_plugins_check_plugin_authenticated_rce` we were able to obtain a root shell using the following options

![[Pasted image 20220627234117.png]]

## Root flag

![[Pasted image 20220627234259.png]]

