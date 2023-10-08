# Blocky

10.10.10.37

A port scan reveals ports 21,22,80, and 25565 are open.

## Port 80

The webserver is hosting a wordpress page. This appears to be a minecraft server which is under contruction. We see a few references to a "Custom Plugin".

Dirbuster finds a `/plugins/` directory, so we navigate to it and are met with 2 plugins that can be downloaded.

We use [JD-GUI](http://java-decompiler.github.io/) to decompile the `BlockyCore.jar` file.

Here is the source code:

```java
package com.myfirstplugin;

public class BlockyCore {
  public String sqlHost = "localhost";
  
  public String sqlUser = "root";
  
  public String sqlPass = "8YsqfCTnvxAUeduzjNSXe22";
  
  public void onServerStart() {}
  
  public void onServerStop() {}
  
  public void onPlayerJoin() {
    sendMessage("TODO get username", "Welcome to the BlockyCraft!!!!!!!");
  }
  
  public void sendMessage(String username, String message) {}
}

```

We try to login to wordpress, phpadmin, and ssh using the credentials from the file:

>Username: root
>Password: 8YsqfCTnvxAUeduzjNSXe22

This doesn't work. But we'll hang onto these incase we need them later.

## Hunting for a user.
Wordpress's login page discloses if the username exists or not, so we can use hydra to find a valid username. We end up finding `notch` as the username.

Suprisingly, we're able to ssh in as notch using the password we found above.

## Privesc
The first thing I do when I get a shell on linux is `sudo -l`. In this case we have access to everything. So root is as simple as `sudo su`

## Flags
We find flags at:
`/home/notch/user.txt` and `/root/root.txt`
