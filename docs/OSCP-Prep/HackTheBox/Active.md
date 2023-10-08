# Active
10.10.10.100

From the scans, we see that SMB is open and allows anonymous access.

We grab a Groups.xml file from the `Replication` share and find encrypted credentials for `SVC_TGS` account.

There is an encrypted password in the file, but we were able to decrypt it using `gpp-decrypt`.

We don't get shell access with this account, but we're able to request a TGS ticket and crack the Administrator password.

