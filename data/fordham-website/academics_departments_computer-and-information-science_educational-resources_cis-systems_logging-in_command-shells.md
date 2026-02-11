https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/command-shells

# Command Shells

The command shell is the program that handles your interaction with the system. Unless you requested otherwise when you were given your account, your login shell is `tcsh`

. The `tcsh`

program is an enhanced version of the `csh`

program, which is described in some Unix texts. The `tcsh`

shell differs from the Bourne shell `sh`

in some respects. Since most texts assume you are using `sh`

, you may find that some commands do not work as stated. Most of the differences have to do with advanced features, so beginners should not have any difficulties. Full documentation of `csh`

, `tcsh`

, `sh`

and `bash`

(an enhanced version of `sh`

) can be found in the
online manual pages, or any comprehensive book on Unix.

The main advantages of the `tcsh`

program are its command and filename completion feature, and the ability to recall and edit commands. To use command and filename completion, type the beginning characters of the desired word, then hit the *tab* key. If only one word matching what you typed is found, the complete name will be filled in. Otherwise you will be prompted with the possible completions. You can recall earlier commands using the up-arrow key, and you can edit a command line by using the left- and right-arrow keys, the *delete* key, and typing replacement text. You can also edit the command line using Emacs-style commands.

*Other shells:* The standard Bourne shell `sh`

is the original Unix command shell. An improved version which includes command recall and editing is called `bash`

(Bourne-again shell).