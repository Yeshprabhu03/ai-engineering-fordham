https://www.fordham.edu/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/passwords

# Passwords

When your `erdos`

account was created, you were given an initial password. The first thing you should do is to change the password. You can do this from a command-line shell using the `yppasswd`

command.

To get a command-line shell, either log on to one of the Linux systems in the computer lab and select *Terminal* from the *Applications/System Tools* menu, or else log in remotely using a
[Secure Shell connection](/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/access-from-internet/connection-using-secure-shell/).

If you would rather not deal with the `yppasswd`

command, you can use the webmail server to change your password. For accounts on `storm`

, point your browser at [https://storm.cis.fordham.edu/webmail](https://storm.cis.fordham.edu/webmail); for accounts on `erdos`

, use the URL [https://dsm.dsm.fordham.edu/webmail](https://dsm.dsm.fordham.edu/webmail). Once logged in, each webmail system has a mechanism for changing your password.

**SquirrelMail**

click on the `Options`

link in the navigation area at the top of the screen and then click on `Change Password`

.

It is important to choose a password that can not be easily guessed. Don't imagine that this matter is unimportant just because you have nothing sensitive or valuable in your account. Unix servers are favorite targets of hackers, because they can use them as a base of operations for attacking other computers. Therefore it is important for all of our users to take security seriously.

Your password should be at least 8 characters long. Avoid choosing a password that is an English or foreign-language word, a person's or pet's name, your login name, your social security number, etc. Those are the first things that hackers guess. Note that upper and lower case letters are distinguished in Unix passwords, and your password should include some of both. Punctuation is also allowed (and encouraged). More suggestions are available in the document
[Selecting Good Passwords](/academics/departments/computer-and-information-science/educational-resources/cis-systems/logging-in/selecting-good-passwords/).

If you would like to be reasonably sure that your password is strong enough to resist casual hacking, you should visit the * Password Checker* page, which will evaluate the strength of your password.

If you have **forgotten or lost** your password, you can use the [cryptpass](https://dsm.dsm.fordham.edu/cgi-bin/cryptpass.pl) web page, which will do the following:

- It gives you the opportunity to check the strength of your new password, via the
page.[Password Checker](http://archive.geekwisdom.com/dyn/passwdmeter.html) - It gives you instructions for
*safely*forwarding your new password to our system administrators, who will install your new password at the earliest opportunity.

**Important note:** Most email is insecure and unencrypted. You should *never* send a password to* anybody* via email. (This also applies to social security numbers, credit card numbers, and so forth.)