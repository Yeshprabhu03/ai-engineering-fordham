https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/customizing-your-environment

# Customizing Your Environment

Your home directory contains default versions of several files that affect the behavior of various programs:

`.cshrc`

--startup script for `csh`

shell program

`.tcshrc`

--startup script for `tcsh`

shell program

`.profile`

--startup script for `sh`

, `bash`

and `ksh`

shell programs

`.login`

--script for `csh`

and `tcsh`

log-in actions

`.emacs`

--startup commands for `emacs`

editor

`.xsession`

--startup script for X-windows session

`.Xdefaults`

--parameter settings for X-windows session

Edit them to customize your environment. You also might want to create the file:

`.plan`

--description of yourself for `finger`

command


(The leading dot in these filenames prevents their being listed by `ls`

unless you use the `-a`

or `-A`

option).