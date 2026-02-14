https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/access-from-internet/obtaining-an-ssh-client

# Obtaining an SSH Client

Both Linux and Mac OS X are equipped with a command-line SSH client, which can be used from within the *Terminal* application. Simply type the command: `ssh username@hostname`

to connect to the specified host. If you want to run[ X-Windows](https://en.wikipedia.org/wiki/X_Window_System) applications, you'll want to allow *trusted X11 forwarding*, which is done via by adding the `-Y`

option to `ssh`

as such: `ssh -Y username@hostname`


Note that Linux comes with the X-Window System already installed. However, Mac OS X users will need to obtain an X-Windows software such as [XQuartz](https://www.xquartz.org/). You will still need to type `ssh -Y`

to enable X-Windows. A quirk with XQuartz is copy and paste works with the center button of a 3-button mouse. For ;mice that do not have 3 buttons, open Preferences and within Input check the box for "Enable three button mouse" and then you will have to hold the Option or Command key and then clicking the right mouse button. Also, updates to the software usually require a system reboot.

For Windows systems, a good Secure Shell client is [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html). However, X11 forwarding no longer works without installing an additional X-Windows client such as [Xming](https://sourceforge.net/projects/xming/files/Xming/6.9.0.31/Xming-6-9-0-31-setup.exe/download) and remembering to enable [X11 forwarding](http://www.geo.mtu.edu/geoschem/docs/putty_install.html). Another great free alternative is [MobaXterm](http://mobaxterm.mobatek.net/download-home-edition.html) which has a built-in X11 server as well as SFTP. Note that both by default disable the blinking of the cursor when logging in but anything you type is being captured. Using Mobaxterm with `ssh -X`

or `ssh -Y`

, you might notice emacs opens with a small window. You can use emacs-gtk2; [read these instructions to compile it](https://storm.cis.fordham.edu/~rkudyba/LC-lab-installation#emacs).