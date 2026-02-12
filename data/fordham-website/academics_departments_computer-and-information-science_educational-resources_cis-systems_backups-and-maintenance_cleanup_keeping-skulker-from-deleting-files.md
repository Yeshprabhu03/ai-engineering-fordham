https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/backups-and-maintenance/cleanup/keeping-skulker-from-deleting-files

# Keeping Skulker from Deleting Files

Here is how to prevent `skulker`

from deleting files you want to keep. Apart from the obvious answer of avoiding ''junk'' names for precious files, there are two standard answers to this.

- Read-only permission. By default, files generally are created with owner-write permission. If you turn off this permission,
`skulker`

will leave the files alone. You can see what permission a file has by using the ''`ls -l`

'' command. For example, if you see this:

`-rw-r--r-- 1 joeuser students 8165 Mar 20 16:47 foo.o`


-r--r--r-- 1 joeuser students 4060 Mar 20 17:14 bar.o

`foo.o`

has owner-write permission turned on, and`bar.o`

has it turned off. To turn off write permission on`foo.o`

, just use the command ''`chmod -w foo.o`

''. To turn write permission back on, change the ''`-w`

'' to ''`+w`

'' in that command.

- Special directories. Executable files are protected from deletion by
`skulker`

if they are located in certain special directories, namely any directory named ''`bin`

'', ''`sbin`

'', ''`cgi-bin`

'', ''`lib`

'', or ''`libexec`

''. Object files are protected if they are in a directory named ''`lib`

''. MPEG files are protected if they are in a directory named`public_html`

. Files are also protected in any subdirectory of one of these directories.


If you have a favorite executable program that you want to keep permanently, the best thing to do is to create a ''`bin`

'' directory in your home directory and place the executable there. To make this program accessible no matter what directory you are in, add ''`$HOME/bin`

'' to your path. This step is easily accomplished by editing the file`.cshrc`

in your home directory.

Finally, don't panic! `skulker`

has no interest in deleting C source files, Perl programs, mailboxes, text files, html files, etc. These can be left lying around for as long as you wish.