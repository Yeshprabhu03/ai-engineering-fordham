https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/access-from-internet/remote-desktop-connection

# Remote Desktop Connection

You can connect to your Linux desktop from any Mac or PC by downloading [X2Go](http://wiki.x2go.org/doku.php). You will need to choose the MATE (pronounced "mah-tay") or XFCE desktop enabled via the "Session type" dropdown. For best performance, go to the "Media" tab, uncheck the "Enable sound support" box and also uncheck "Client side printing support". This displays your desktop, similiarly as if you logged in directly in the lab, but does so on any computer with an Internet connection.

Then enter either `storm.cis.fordham.edu`

or `erdos.dsm.fordham.edu`

depending on where your account is located.

When finished with your remote session, you can log out by clicking "System" and choosing "Log Out " and the remote desktop will close.

**Troubleshooting:** The most common cause of a failure to start the remote desktop is the existence of a remote communication process left over from a previous connection. To fix this, use a
[Secure Shell connection](/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/access-from-internet/connection-using-secure-shell/) to open a shell session on the remote server and give the command `pkill -9 -u <your-user-name>`

. Note that this will also force-quit the SSH session and `<your-user-name>`

should be your actual erdos or storm username. If that does not work, you can also delete the `.x2go`

directory in your home directory with the command `rm -rf .x2go`

.

A [known issue](https://github.com/ArcticaProject/nx-libs/issues/600#issuecomment-383088734) is using the full screen option from Windows and dual monitors. Downlaod and install [VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/).