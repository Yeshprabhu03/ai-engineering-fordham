https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/electronic-mail/reading-and-sending-unix-mail

# Reading and sending Unix mail

The standard Unix electronic mail program, [ mail](https://linux.die.net/man/1/mail), is very primitive and difficult to use. We recommend that you use one of the following methods of handling your electronic mail:

[emacs](/academics/departments/computer-and-information-science/educational-resources/cis-systems/electronic-mail/accessing-fordham-email/accessing-unix-mail-with-emacs/),

[alpine](/academics/departments/computer-and-information-science/educational-resources/cis-systems/electronic-mail/accessing-fordham-email/accessing-unix-mail-with-alpine/), or

[SquirrelMail](/academics/departments/computer-and-information-science/educational-resources/cis-systems/electronic-mail/accessing-fordham-email/accessing-unix-mail-via-a-web-interface/). More details are given in the following sections.

These methods of reading your mail access it directly on the Unix host, and store saved mail in folders on that host. If you want to use a Web browser such as Microsoft Internet Explorer or Firefox to read and store your Unix mail on your home computer, then you need to use the POP or IMAP protocol to fetch your mail. Because of the security hazards of reading mail from a browser on a Windows computer, POP access is not supported on the Department's servers. They do support IMAP access using SSL for security.

If your mail client only supports POP or non-SSL IMAP, then in order to read your Unix mail you must forward it to the Fordham University mail server (using the method described in
[the previous section](/academics/departments/computer-and-information-science/educational-resources/cis-systems/electronic-mail/forwarding-your-unix-mail-to-another-address/)) and use POP to access it there. This server scans all mail for known viruses and other hostile content, rendering it safer (but not safe!) for this mode of access.

To send mail to another user on a local Unix host, the address is simply the username, e.g. `joeuser`. To send mail to a user on another host on the campus net, the address must include the username and node name, e.g. ` [email protected]`. To send mail to a user elsewhere on the Internet, the address must include the full internet address, e.g.

`.`

[[email protected]](/cdn-cgi/l/email-protection)The usual method is to compose and send a message using one of the mail-handling programs described in the next sections. It is also possible to mail an existing text file using the Unix [ mail](https://linux.die.net/man/1/mail) program:

`mail` *to-address* `<` *filename*

where the *to-address* is the address (in one of the forms described in the previous paragraph) of the user to whom you wish to send the file, and *filename* is the name of the file to send. For instance, to send a copy of your program `hello.cc` to your instructor, whose user name is `janeprof` on the local host, you would type:

`mail janeprof < hello.cc`