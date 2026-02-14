https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/disk-quotas

# Disk Quotas

Student accounts on `erdos`

are subject to disk quotas. The purpose of these quotas is to avoid having the user disk fill up, which prevents everyone from getting any work done. The disk space currently available is ample, so generally the disk fills up only when someone is irresponsible or some software goes haywire. Therefore, the quotas are set at 1 GB. This limit is low enough to ensure that no single user can fill up the disk, but high enough that most users should never run up against it.

However, if a number of users were to reach their quotas simultaneously, the disk could still fill up. Therefore, we ask users to be thoughtful of others, and try to keep their usage of the disk to a reasonably low value, say 500 MB or so. You can check your disk usage and quota status by using the command `quota`

. (The amounts shown by the `quota`

program are in blocks of 1 KB.)

If you see an error such as:

`E297: Write error in swap file "xx.cpp"`


E667: Fsync failed

This can indicate you have exceeded your quota.


Also, in LL612, if you notice when logging in the screen goes back to the username prompt, this also indicates going over the quota.

If you have an important reason for going above the standard disk quota, contact the system administrators at [[email protected]](/cdn-cgi/l/email-protection#4c2429203c0c283f21622a233e28242d2162292839), and explain your need, and they can increase your quota.

**Note** that if you have filled your quota, you will not be able to save any more files. Moreover, you may not be able to log in via the graphical interface. Should this happen, you can use the `du`

(*disc usage*) command will help you find large directories and/or files. Do the following:

- Set your computer to use text mode, rather than graphical mode. If you're in the computer lab, set your computer to use text mode. You can do this by simultaneously holding down the
*Ctrl*,*Alt*, and*F1*buttons. If you're using a remote connection:- From a Mac or Linux machine, open a Terminal and connect using
`ssh`

*without*the`-Y`

option. - From a Windows machine, use a text-based SSH client, such as PuTTY or MobaXterm.

- From a Mac or Linux machine, open a Terminal and connect using
- Log in.
- Use the
`du`

command to look for disk hogs, using the commands:`du -sh * .[a-zA-Z]* | sort -nr`

. If you get a lot of results, you may need to pipe this through`more`

or`head`

. - If you find an unexpectedly large directory,
`cd`

into that directory and do ''`ls -l`

''. Delete any large files that you know you don't need. - If a large directory has subdirectories, go back to step 2 above, so that you can examine its subdirectories for disk hogs.
- Log out.

Here are some typical disk hogs.

- The "
`~/.cache`

" directory. This can be deleted straightaway without ill effect with the following command:`rm -rf ~/.cache`


- Firefox cookies and cache
- Click the menu button

and choose Options. - Select Library.
- Select History.
- Click Clear Recent History and then click Clear Now.

- Click the menu button
- If you prefer delete the cookies from terminal you can use the following command:
-
`rm ~/.mozilla/firefox/*.default*/cookies.sqlite`


-
-
To clean all the Firefox cache, you can use these 3 commands:

`rm -r ~/.cache/mozilla/firefox/*.default*`

`rm ~/.mozilla/firefox/*.default*/sessionstore.js*`

`rm ~/.mozilla/firefox/*.default*/*.sqlite`



We also try to conserve disk space by running skulker to clean up unused junk files in users' directories. See the
[Cleanup](/academics/departments/computer-and-information-science/educational-resources/cis-systems/backups-and-maintenance/cleanup/) section for details.