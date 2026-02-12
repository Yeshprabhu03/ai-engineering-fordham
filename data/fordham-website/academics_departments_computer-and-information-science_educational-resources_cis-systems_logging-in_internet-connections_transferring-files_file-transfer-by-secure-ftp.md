https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/internet-connections/transferring-files/file-transfer-by-secure-ftp

# File Transfer by Secure FTP

In order to transfer files between your home computer and the Unix host, you should install a secure shell file transfer client.

In the computer laboratory, the Windows systems have the Secure Shell File Transfer Client installed. This client is no longer supported by its maker, but it is still usable. Directions for using it are in the
[next section](/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/internet-connections/transferring-files/secure-shell-file-transfer/).

We recommend that you use FileZilla, which runs on Windows, Mac OS X, and Linux systems. It is available for free download from [http://filezilla-project.org/](https://filezilla-project.org/). You need only the FileZilla Client application.

By default, FileZilla uses the old, unsecure ftp protocol. To make it use the secure protocol (which is the only one accepted by `erdos`

), you must prefix the host name in the Host box with `sftp://`

, for example `sftp://erdos.dsm.fordham.edu`

. Enter your username and password in the boxes, the same ones you use for logging in on `erdos`

or `storm`

. Leave the Port box blank. Hit Quickconnect.

The FileZilla screen is divided into several areas. The top text area gives status information. Any error messages related to connecting will appear here. Below that are two columns, showing local directories (folders) and files on the left and remote directories and files on the right. The right-hand display will be blank until you have successfully connected. The upper boxes of each pair show the directory trees on both hosts, and the lower boxes show the files and directories within the currently selected directory. You can use the directory trees to navigate quickly to other locations, but you may prefer to hide them (using the View menu) and navigate only with the directory and file view.

To transfer a file from one host to the other, find it and right-click on it, then select Upload (to remote host) or Download (from remote host).

The upload/download status is shown in an area at the bottom of the FileZilla screen.

Once you are finished transferring files, use the Server menu or click on the red X icon to disconnect from the remote system.

Normally FileZilla shows all files and directories, including hidden ones (which, on the Linux side, have names starting with a dot). There are a lot of these in your Linux home directory, so you will need to scroll past them to reach the files and directories of interest. To suppress these, you can define and then apply a filter. Here's how:

- From View menu select Filename filters, and click on Edit filter rules.
- In Edit filters, click New. Name the new filter appropriately, e.g. "Suppress unix hidden files". For Filter conditions, choose ''Filter out items matching all of the following.'' Create a single condition: in the first box, choose ''Filename''. In the second box choose ''begins with''. In the third box put just a period (dot). Click OK.
- You can now enable or disable the filter using the View menu, Filename filters and checking or unchecking the box next to the filter name to enable it. (This filter only suppresses hidden files on Unix-type hosts, not Windows hosts, which use a different mechanism for hiding files.)