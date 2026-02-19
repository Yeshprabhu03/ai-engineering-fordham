https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/backups-and-maintenance/backups

# Backups

All user home directories and mailbox files are backed up regularly to a large hard drive, as ''snapshots'' that capture the file system at specific times. Currently, a snapshot is taken each day at 3 a.m., then every two hours from 10 a.m. - 8 p.m. (Because it takes some time for files to be copied, the exact time of the snapshot may be anywhere within about 5 minutes before or after the hour.) Snapshots are retained throughout the day, and then copies are kept of the 3:00 am snapshots each day for a week, on Sunday each week for four weeks, and on the first of each month for three months.

If you accidentally delete or corrupt an important file, you can easily recover it from a snapshot. The snapshots are stored in directory `/snapshots/`

on all the local hosts. You can browse this directory either using the command `ls /snapshots/`

from a shell command-line, or by double-clicking on the Computer icon on the desktop, opening Filesystem, and then opening snapshots. Within this directory you will find sub-directories named `hourly.0`

through `hourly.6`

(containing the most recent snapshots made), `daily.0`

through `daily.6`

containing the snapshots retained each day, and likewise for the weekly and monthly snapshots.

Choose the snapshot you want based on its date, selecting a snapshot made after the file was created and before it was lost. (Use `ls -lt /snapshots/`

from the command line to list the snapshots by date in order, or in a graphical file browser select View as List and sort by Date Modified.)

Now, if you are working from a command line, simply append `/var/www/jadu/public_html/`

to the path constructed from `/snapshots/`

followed by the chosen snapshot directory, and you will have your home directory.

For example, if you accidentally deleted a file named `foo.cc`

in your `private/cs1`

directory, and supposing the last good copy is in the `hourly.3`

snapshot, you can recover your file by going into your `private/cs1`

directory and giving the command `cp /snapshots/hourly.3//var/www/jadu/public_html//private/cs1/foo.cc .`


That's all there is to it! (Note that hitting the tab key after typing part of a path component will complete it for you, saving you typing and avoiding typing errors.)

If you are using a graphical file browser, getting to your home directory is slightly more complicated. In this case, open the chosen snapshot directory, where you will see two directories: `u`

and `s`

. The `u`

directory is where user files are stored, while `s`

contains system files. Descend into the `u`

directory and then into the directory named for the host where your home directory lives. (This is `erdos`

for most students.) From there, undergraduate students open the `students`

directory while graduate students open the `csga`

directory. There you will find your home directory with your login name. Go into the directory where your lost file is, and drag it to where you want to restore it.

If you have any trouble following these instructions, please contact one of the system administrators at [[email protected]](/cdn-cgi/l/email-protection#177f727b675773647a39717865737f767a39727362), and they will help you to restore the file.