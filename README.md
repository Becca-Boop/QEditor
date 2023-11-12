# QEditor

An editor for QuestJS

This is in a fairly early stage of development, so do not expect too much yet! It should be useable on Unix and MacOS, though I have only tried on Windows as that is all I have.

It is written in Python using Django, and is run as a web server. Once it is up and running, access it via your browser. Help files are included, and accessed from within it.

To run it you will need to download Python and Django. Download Python from here, if you do not already have it:
https://www.python.org/downloads/

Check it works by typing "python" at a command line. it should take you to an interactive session, and tell you the version. Type "exit()" to get out of that. Back at the command line, you should now be able to install Django:

python -m pip install Django

Then go to the folder you install QEditor:

python manager.py runserver 3000

Now open up yuour browser, and go to http://localhost:3000

QuestJs can be found here:
https://github.com/ThePix/QuestJS/wiki

