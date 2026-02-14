https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/text-editors/using-emacs

# Using Emacs

A [hypertext introduction to emacs](http://www.tldp.org/HOWTO/Emacs-Beginner-HOWTO.html) is available.

If you're working in X-windows, you can choose `emacs`

from the *Applications* menu (under *Accessories*). You can also run `emacs`

by typing either of the following two commands in a terminal window: ` emacs & `

or (to immediately start editing `filename`

): `emacs filename &`


*Note the ampersand & appearing at the end of the line!* This is important when you are working in X-windows, since it runs `emacs`

in the background, meaning that you can run other commands from your terminal window. If you forget the ampserand, you can put `emacs`

into the background by first suspending it (giving it the `C-x C-z`

command key sequence) and then typing the `bg`

command into the shell window.

However if you're *not* working in X-windows (e.g., you're using a simple text-based terminal from home) do *not* put the ampersand at the end of this line. Doing so will tie up your terminal, which will be waiting for emacs until such time as you bring it into the foreground by typing the `fg`

command.

The `emacs`

program comes with a tutorial. Once you have started up `emacs`

, hit the help key (normally control-`h`

or control-`?`

) followed by the letter `t`

to begin the tutorial. Alternatively, you can start up `emacs`

in tutorial mode by giving the command `emacs -f help-with-tutorial`


You can suspend `emacs`

by pressing `control-X`

and then `control-Z`

. Resume it with the `fg`

command.

Exit from `emacs`

using `control-X control-C`

.

Using Mobaxterm with `ssh -X`

or `ssh -Y`

, you might notice emacs opens with a small window. You can use emacs-gtk2; use [these instructions to compile it](https://storm.cis.fordham.edu/~rkudyba/LC-lab-installation#emacs).