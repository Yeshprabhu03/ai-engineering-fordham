https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/creating-student-accounts

# Creating Student Accounts

### September 2021 update: Banner can no longer be used to create the student input file. Instructions have been updated below for use in Blackboard.

### Lincoln Center (erdos) / Rose Hill (storm):

All faculty with staff accounts on the **dsm** and **storm** servers can create student accounts there. The script will print account cards that contain their login credentials that can be handed to students.

**Note:** we use the sudo mechanism to grant non-root users authority to create users. The first time you use one of the scripts for this purpose, you will be given a short warning about responsible use of the sudo mechanism. Each time you run the scripts, you will be asked for a password. This will be your regular login password on **storm** or **erdos** (or **dsm**).

**Important:** for the **erdos** server, you must be logged in on **dsm**, to create accounts. Network Information Service (NIS) runs on **dsm** (but not **storm**). You can log in to `dsm`

from `erdos`

by running `ssh dsm`

.

- Prepare the input file for the
`create-accounts`

script. We will assume it is named`classlist.txt`

. If you are doing this outside the server, you will have to SFTP, e.g., with MobaXterm/Filezilla, or use a text editor (vi, emacs, nano, notepad) to copy and paste the contents of the HTML page.- If you are creating accounts for an entire class, it is convenient to create the input file from your class roster via the
[fordham.edu](http://fordham.edu/)portal, preferably with Firefox or Chrome. The following are the new instructions in Blackboard.- Log in to Blackboard
- Navigate to course home page
- Use Course Management Control Panel to open Grade Center, Full Grade Center
- Click on Work Offline, select Download
- Select Data to Download: User Information Only
- Select Options Delimiter Type Tab, Include Hidden Information No
- Submit, Download, save file (default extension is .xls, but the file is a CSV).
- Then run:
`accts-from-bb-roster filename.csv > classlist.txt`



- Alternatively, by hand, use any text editor to create the text file
`classlist.txt`

with each account to be created on a separate line. The line begins with the username to be given to the user. This cannot have blank spaces. By convention, we use lowercase usernames, generally consisting of the left side of the user's @fordham.edu address. After the username, put a blank or tab, then the user's real name. Optionally after that put the user's preferred email address to which local Unix mail will be forwarded. A typical line might look like this:`bovik Harry G. Bovik`

[[email protected]](/cdn-cgi/l/email-protection)

- If you are creating accounts for an entire class, it is convenient to create the input file from your class roster via the
- Feed the input file into the account creation script. Note that we reccommend you use
`-test`

(to see what will happen and check for existing usernames) and/or`-help`

before the filename.`$ create-accounts -test classlist.txt`


If the class is a graduate class, include the option`-csga`

before the filename, so the accounts will be created in the csga directory. The account cards are printed on the default printer, which in LC is the HP LJ in room LL 612 and the HP LJ in JMH 302. - To specify a different printer, for instance
**ps610-c**, include the option`-Pps612`

but the filename should be the last option in the command so it would look like this:`create-accounts -Pps612 classlist.txt`

- Available Printers
- LC
**ps612**HPLJ P3015 in LL 612 (*default*)**ps610-c**HP color LJ in LL 610 hallway**ps813**HPLJ P4014dn in LL 813

- RH
**jmh302**, JMH 302 (*default*)


- LC

- Available Printers
- If you'd prefer to "print to a file" you then use the -P- option like this:
`$ create-accounts -P- classlist.txt`


And that will print to a local file in your current directory called`lpr`

. - The script may report that some users already may exist. If their email address does NOT end in @fordham.edu (sometimes an @gmail.com appears in Banner), you can use the left side of their email address. i.e., the username. If the username exists and is not an obvious duplicate, use a CLI text editor to remove them from the input file. If it is simply a case of two students with the same last name, edit the file to change the username, for instance by prefixing it with the user's first initial. For instance, if username bovik is already taken, the input line in the example above could be changed to specify
`hbovik`

as the username instead. After correcting the input file, re-run the account-creation script. - To reset a user password and have it print a new account card run the following command:
`sudo gen-account-cards -Pps612`

*username*- where
is the actual student username and`username`

`-P`

can be any printer from the above list. `-P-`

will allow you to create a local file in your current directory called`lpr`

(as in #4 above), e.g.,`sudo gen-account-cards -P-`

.*username*- Note from
`dsm/erdos`

there can be a 5 minute delay before the pasword change takes effect. - The
`storm`

server has a script called`changepasswordof`

that can be run from any ssh session by a professor.

- where