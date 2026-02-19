https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/access-from-internet/connection-using-secure-shell

# Connection Using Secure Shell

Secure Shell provides an encrypted channel for all data between your computer and the Unix host. Encryption is used even for the log-in process, so that your password cannot be captured off the Internet. SSH access is enabled to all the Computer Science Department servers.

Information about how to get an SSH client is described in the
[next section](/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/access-from-internet/obtaining-an-ssh-client/). Once you have connected to the ISP and established the network connection, simply start the SSH client. Once the SSH client is running, you must specify the complete host name to connect to, including the domain name, i.e., `storm.cis.fordham.edu`

for `storm`

or `erdos.dsm.fordham.edu`

for `erdos`

.

You will then be prompted for your username and password. Type these exactly as they are given on the account information sheet. (The password will not appear when you type it.) Note that in Unix, upper and lower case are *not* considered equivalent.

Note that SSH provides only a text-based connection, with no graphics or mouse support. However, if you run X-windows at home (e.g. by running Linux on your home computer, or by running an X-windows application under Windows or Mac OS X), you can tunnel X traffic between the departmental host and your home system through the SSH connection. (The manner in which this is done depends on the client. Consult the client's documentation for details.) This allows you to launch a remote application such as emacs and have it appear in a window on your Linux desktop. You should do this only if you have a high-speed Internet connection; otherwise the performance will be very sluggish.

To log out of your SSH session, at the shell prompt type the command `logout`

and hit the *Enter* key.