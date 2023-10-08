# Bastard
`Still in progress`
## Recon  

The tags for [this box](https://app.hackthebox.com/machines/7) are:  
> - Windows
> - PHP  
> - Patch Management
> - Web

Difficulty:
> Medium

Port scan revealed webserver on port 80, RPC on 139 and 49154.
The webserver has Drupal 7 running on IIS 7.5

### Enumerating the webserver

There are some interesting entries in `robots.txt`:  

```bash
# Directories
Disallow: /includes/
Disallow: /misc/
Disallow: /modules/
Disallow: /profiles/
Disallow: /scripts/
Disallow: /themes/
# Files
Disallow: /CHANGELOG.txt
Disallow: /cron.php
Disallow: /INSTALL.mysql.txt
Disallow: /INSTALL.pgsql.txt
Disallow: /INSTALL.sqlite.txt
Disallow: /install.php
Disallow: /INSTALL.txt
Disallow: /LICENSE.txt
Disallow: /MAINTAINERS.txt
Disallow: /update.php
Disallow: /UPGRADE.txt
Disallow: /xmlrpc.php
# Paths (clean URLs)
Disallow: /admin/
Disallow: /comment/reply/
Disallow: /filter/tips/
Disallow: /node/add/
Disallow: /search/
Disallow: /user/register/
Disallow: /user/password/
Disallow: /user/login/
Disallow: /user/logout/
# Paths (no clean URLs)
Disallow: /?q=admin/
Disallow: /?q=comment/reply/
Disallow: /?q=filter/tips/
Disallow: /?q=node/add/
Disallow: /?q=search/
Disallow: /?q=user/password/
Disallow: /?q=user/register/
Disallow: /?q=user/login/
Disallow: /?q=user/logout/
```

There are also some interesting findings by feroxbuster

```bash
200      159l      413w     7583c http://10.10.10.9/0
200      159l      413w     7583c http://10.10.10.9/node
200        1l        7w       62c http://10.10.10.9/rest
200       90l      243w     2189c http://10.10.10.9/robots.txt
200      152l      394w     7420c http://10.10.10.9/user
200      159l      413w     7583c http://10.10.10.9/0
200      159l      413w     7583c http://10.10.10.9/index.php
200       45l      262w     1717c http://10.10.10.9/install.mysql.txt
200       44l      290w     1874c http://10.10.10.9/install.pgsql.txt
200      159l      413w     7583c http://10.10.10.9/node
200        1l        7w       62c http://10.10.10.9/rest
200       90l      243w     2189c http://10.10.10.9/robots.txt
200      152l      394w     7420c http://10.10.10.9/user
200        1l        6w       42c http://10.10.10.9/xmlrpc.php
200      152l      394w     7420c http://10.10.10.9/user
200      159l      413w     7583c http://10.10.10.9/node
200      159l      413w     7583c http://10.10.10.9/
200      159l      413w     7583c http://10.10.10.9/0
200      175l      510w     9063c http://10.10.10.9/User
200        1l        7w       62c http://10.10.10.9/rest
200        1l        7w       62c http://10.10.10.9/REST
200      175l      510w     9063c http://10.10.10.9/USER
200      123l      714w     5382c http://10.10.10.9/ReadMe.txt

```

## NMAP port scan
```text
PORT      STATE SERVICE REASON          VERSION                                                                                                                              80/tcp    open  http    syn-ack ttl 127 Microsoft IIS httpd 7.5                                                                                                              | http-robots.txt: 36 disallowed entries                                                                                                                                     | /includes/ /misc/ /modules/ /profiles/ /scripts/                                                                                                                           | /themes/ /CHANGELOG.txt /cron.php /INSTALL.mysql.txt                                                                                                                       | /INSTALL.pgsql.txt /INSTALL.sqlite.txt /install.php /INSTALL.txt                                                                                                           | /LICENSE.txt /MAINTAINERS.txt /update.php /UPGRADE.txt /xmlrpc.php                                                                                                         | /admin/ /comment/reply/ /filter/tips/ /node/add/ /search/                                                                                                                  | /user/register/ /user/password/ /user/login/ /user/logout/ /?q=admin/                                                                                                      | /?q=comment/reply/ /?q=filter/tips/ /?q=node/add/ /?q=search/                                                                                                              |_/?q=user/password/ /?q=user/register/ /?q=user/login/ /?q=user/logout/                                                                                                     | http-methods:                                                                                                                                                              |   Supported Methods: OPTIONS TRACE GET HEAD POST                                                                                                                           |_  Potentially risky methods: TRACE                                                                                                                                         |_http-title: Welcome to 10.10.10.9 | 10.10.10.9                                                                                                                             |_http-generator: Drupal 7 (http://drupal.org)                                                                                                                               |_http-favicon: Unknown favicon MD5: CF2445DCB53A031C02F9B57E2199BC03                                                                                                        |_http-server-header: Microsoft-IIS/7.5                                                                                                                                      135/tcp   open  msrpc   syn-ack ttl 127 Microsoft Windows RPC                                                                                                                49154/tcp open  msrpc   syn-ack ttl 127 Microsoft Windows RPC                                                                                                                Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port                                                                        Device type: specialized|general purpose|phone                                                                                                                               Running (JUST GUESSING): Microsoft Windows 7|8|Phone|2008|8.1|Vista (91%)
```

## Services

### Port 80
#### IIS 7.5
#### Drupal 7


### Port 135

### Port 49154