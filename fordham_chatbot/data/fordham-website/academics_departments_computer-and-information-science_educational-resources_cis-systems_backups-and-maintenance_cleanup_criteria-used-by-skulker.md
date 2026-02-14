https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/backups-and-maintenance/cleanup/criteria-used-by-skulker

# Criteria Used by Skulker

Here are the criteria skulker uses to determine whether a file is probably junk and therefore a candidate for deletion.

- Junk Names:
- Any name ending in a tilde (~) character. Emacs uses this to name backups of files you edit.
- Any name beginning and ending with the pound (#) character. Emacs uses these for checkpoint files in case it or the system crashes unexpectedly, or you lose your connection in the middle of an editing session.
- The name ''
`ed.hup.`

'' This is the name given by`ed`

to a backup file it creates when you lose your connection in the middle of an editing session. (We hope you are not still using ed.) - The name ''
`a.out.`

'' This is the default name for the result of compiling a program. Usually programs are given meaningful names, so`a.out`

is probably something temporary. (These files are identified as junk only if they are executable.) - The name ''
`core`

'', or a name of the form ''`core.`

'' followed by an integer. This is the name of a core dump produced when your program crashes. (In the second form, the integer is the process ID of the program that crashed.)


- Binary executable files:
- Any executable file produced by compilation. These are positively identified as such by looking at the leader to make sure it matches the format of an executable file. Note that Perl programs and shell scripts are not included, even though they have executable permissions, since they are not the result of compilation.


- Any executable file produced by compilation. These are positively identified as such by looking at the leader to make sure it matches the format of an executable file. Note that Perl programs and shell scripts are not included, even though they have executable permissions, since they are not the result of compilation.
- Object files:
- Any file with a name ending in ''
`.o,`

'' which is produced as an intermediate by the compiler when you create a program by separate compilation of several different source files. These are positively identified by looking at the leader to make sure it matches the format of an object file.


- Any file with a name ending in ''
- Transfer files:
- MPEG streaming audio, video, or system files and MS-DOS or Windows executable files are assumed to be files downloaded by the user for transfer to another system. Such files are unusable on
`erdos`

, and so there is no reason for them to remain on the system after they have been copied to their final destination. These files are identified by having a filename extension of ''`.mp3`

'' (upper or lower case) for MPEG files or ''`.exe`

'' (upper or lower case) for DOS/Windows executables, and are positively identified by looking at the leader to make sure it matches.

- MPEG streaming audio, video, or system files and MS-DOS or Windows executable files are assumed to be files downloaded by the user for transfer to another system. Such files are unusable on

Of course, these files are all useful for some period of time, so `skulker`

will not delete them if they have been accessed recently. At present, the age limit is 90 days. If a file which meets the criteria for junk listed above is unused for this long, it becomes fair game. Note that this does not automatically apply if the file merely *is* older than 90 days, but only if it has not been *used* for this period of time. Every time you read or copy a text file, execute a program, or link an object file, its usage time is updated and it becomes safe from `skulker`

for another 90 days. You can see the date of last access of a file by using the ''`ls -lu`

'' command.

Any file that is not in one of the above categories is permanently safe from skulker, no matter how long it has been sitting around.