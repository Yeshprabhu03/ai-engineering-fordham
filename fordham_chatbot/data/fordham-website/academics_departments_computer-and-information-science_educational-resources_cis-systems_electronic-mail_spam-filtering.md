https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/electronic-mail/spam-filtering

# Spam Filtering

Your incoming Unix email is checked for spam. Mail messages that are identified as possible spam are diverted to a file (`Caughtspam`

) in your `mail`

directory. Since spam filtering is not an exact science, there's always the possibility of false negatives or false positives; in other words, spam may be misidentified as legitimate email or vice versa. False negatives are easy to deal with; simply delete the offending message. To deal with false positives, you should check the Subject field of each suspicious message; if they all turn out to be spam, you can safely delete the file containing same.

If you use alpine or SquirrelMail to read your email, the Caughtspam file appears as a mail folder in which you can view the subject lines in the usual way.

If you don't use alpine or SquirrelMail, here's how you can check for false positives:

- Run the command mvspam from a shell window. This safely moves the suspected spam file to a holding directory (
`~/.holdspam/`

). - Run the
`checkspam`

command. If you have an inordinately large amount of spam, you should pipe the results through the`more`

command, i.e., use the`checkspam | more`

command sequence. - If there are no false positives, run the
`rmspam`

command, which will safely delete the suspected spam. It will ask you whether you're sure you really want to delete your spam file; in other words, it gives you a chance to change your mind.

If there are false positives, there are a few things you can do to read the associated email message:

- If you are comfortable reading email in emacs, you can run
`RMAIL`

or`vm`

on the file:- If you want to use
`RMAIL`

, issue the command`C-u M-x`

rmail from within`emacs`

. - If you want to use
`vm`

, issue the command`M-x vm`

from within`emacs`

, followed by the keystroke v. - In either case, when prompted for a file name, enter
`~/.holdspam/Caughtspam`

as your response.

- If you want to use
- If you would rather not read mail from within
`emacs`

, you can use the`more`

command to look at the`~/.holdspam/Caughtspam`

file. You can also examine the file with a text editor that you like. In either case, you would simply scroll down (or do a search) until you find the subject header of interest. - If the spam-filtering software consistently identifies one or more addresses incorrectly as spam sources, you can create a file
`~/.whitelist`

containing those addresses; the spam-filtering software will then assume that any mail coming from said addresses is legitimate.

Of course, once you have done this, you should use `rmspam`

to get rid of the spam.