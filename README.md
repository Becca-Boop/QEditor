# QEditor

An editor for QuestJS

This is in a fairly early stage of development, so do not expect too much yet! It should be useable on Unix and MacOS, though I have only tried on Windows as that is all I have.

It is written in Python using Django, and is run as a web server. Once it is up and running, access it via your browser. Help files are included, and accessed from within it.

To run it you will need to download Python and Django. Download Python from here, if you do not already have it:
https://www.python.org/downloads/

Check it works by typing "python" at a command line. it should take you to an interactive session, and tell you the version. Type "exit()" to get out of that. Back at the command line, you should now be able to install Django:
```
python -m pip install Django
```
Then go to the folder you install QEditor:
```
python manager.py runserver
```
Now open up yuour browser, and go to http://localhost:8000

QuestJS can be found here:
https://github.com/ThePix/QuestJS/wiki

You will need to copy the "assets", "lang" and "lib" folders from there to the "edit/static/edit/" folder to be able to play your game from the editor.

You can make yourself a superuser!
```
python manage.py createsuperuser
```
This will allow you to go to the database admin page. One possible reason to do that is to delete an item, another is to move an item out of a location that no longer exists.


### To-Do List

Some areas for improvement

* Export facility, with versioning and options for play vs beta
* Better script support. Should be possibly to check code if we know what the parameters are. Use Blockly?
* Responses (in the QuestJS sense) - used by ask/tell, reactions and other things
* Easy way to add custom attributes
* Better styling, including icons for links on home page
* Better testing, in particular for views.py
* Multiple game handling
* Use Push API (https://developer.mozilla.org/en-US/docs/Web/API/Push_API) and JSON/XMLHttp to update pages
* Import from Quest 5
* Import from QuestJS
* Multiple users (security being the big issue)
    