https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/electronic-mail/forwarding-your-unix-mail-to-another-address

# Forwarding your Unix mail to another address

In olden times, the customary way of forwarding mail from Unix accounts was by creating a file named `.forward`

in your home directory, containing your preferred e-mail address, to which e-mail should be forwarded. Unfortunately, using the `.forward`

mechanism pre-empts spam processing. In other words, *all* of your mail would be sent to the forwarding address, whether it's spam or legitimate email. This could result in your account being blacklisted as a source of spam, if you receive and automatically forward a lot of it.

Fortunately, there is a way to do the spam checking before forwarding your mail, so that only the mail that is not flagged as spam will be forwarded. All you need to do is to make a small change to the file in your home directory named `.procmailrc`

. The last line of this file normally says `$DEFAULT`

. Remove the `$DEFAULT`

and replace the line by a line containing an exclamation point followed by a blank space and then the destination address. For instance, if your preferred email address is

, the last two lines of [[email protected]](/cdn-cgi/l/email-protection)`.procmailrc`

would be:

`:0:`


! [[email protected]](/cdn-cgi/l/email-protection)