https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/electronic-mail/accessing-fordham-email/accessing-unix-mail-with-emacs

# Accessing Unix mail with Emacs

`Emacs`

has special modes for reading and sending mail. If you are using emacs from an X-windows session, simply use the Tools menu to select Read Mail (with RMAIL) or Send Mail (with GNUS Message). The menu bar gets a Mail menu that provides various functions.

One disadvantage of RMAIL is that it doesn't handle ''rich'' mail (i.e., mail with fancy formatting or attachments) very well. If you tend to get a lot of rich mail, you should consider using the emacs `vm`

(for ''View Mail'') package, which handles rich mail very well. To use same, simply issue the keystroke combination `M-x vm`

.

Now suppose that you are using emacs through a shell connection (such as `ssh`

). Then the mouse won't work for you at all within said session. You can still use the `vm`

pretty much as before. On the other hand, if you want use `RMAIL`

, you'll need to use the keystroke combination `M-x rmail`

to read your mail, and `C-x m`

to send a mail message.

In either case, each of these mail-related modes has its own special key bindings: use `C-_ m`

to get a listing of them.