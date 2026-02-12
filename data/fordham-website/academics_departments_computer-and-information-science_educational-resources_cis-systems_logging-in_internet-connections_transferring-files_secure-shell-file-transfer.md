https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/internet-connections/transferring-files/secure-shell-file-transfer

# Secure Shell File Transfer

These instructions are for the file transfer application from SSH Communications Security Corp., which is no longer publicly available but is installed in the computer lab.

Double click on the SSH Secure Shell File Transfer Client icon on your desktop to start it. You will see your desktop items in a window on the left under "Local Name" and nothing in the window on the right under "Remote Name".

Before you connect for the first time, it is convenient to create a Profile so that you can avoid specifying the connection details each time you connect. Do this as follows:

**Create profile**

Click on Profiles below the toolbar. Select Add Profile... and specify a profile name that characterizes the connection. For instance, if your account is on erdos and your account name is janeuser, you could name the profile ''janeuser@erdos''. Enter the profile name in the box and click on Add to Profiles.**Customize profile**

Now click on Profiles again, select Edit Profile... and click on the name of the profile you just created. The main details you must specify are the host name and user name under the Connection tab. The host name is`erdos.dsm.fordham.edu`

or`storm.cis.fordham.edu`

and the user name is the one printed on the sheet with your account information. In our example, this would be janeuser. Enter these values into the boxes and click on OK to save them in the profile.**Optional customizations**

All other options should be OK if you leave them at the defaults. If later you find that the Delete key does not work as expected, you may re-edit the profile to choose options under Keyboard: either "Delete key sends Backspace" or "Backspace key sends Delete".

Next, to connect to the remote host, first make sure your home computer is connected to the Internet. Click on Profiles and then select the profile you created for connecting to the remote host.

The first time you connect to any given remote host, you will be asked to accept the host key. (This is a security measure to prevent other computers from masquerading as that host.) Answer yes.

A password box will pop up. Enter the password from your account sheet and press Enter or click on OK. You should then see your erdos home directory files appear in the right-hand window under "Remote Name".

You can create a new folder on the remote host by using the Operation menu and selecting New Folder. Type the name of the new folder in the box, for instance `public_html`

, and press Enter.

To put documents into a folder on the remote host, double click on the folder. The current contents (if any) of the folder will appear in the Remote Name window. Next, click on the upward-pointing arrow in the toolbar, which signifies Upload. A file browsing window will appear. Browse around to locate the document(s) that you want to upload. (You can select one or more documents for upload in one operation.) Click on Upload, and you should soon see the file(s) appear in the Remote Name window.

Transferring a document from the remote host to your home computer is similar. Just click on the downward-pointing arrow in the toolbar instead of the upward-pointing one.

There are many other functions that you can perform using the Secure Shell File Transfer Client. The most commonly needed ones are renaming or deleting files and folders. These functions can be found on the Operation menu. Other features can be learned by exploring the various menus.

When you are finished with your file transfer operations, use the File menu to select Disconnect, and then Exit.