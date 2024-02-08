# QEditor

An editor for QuestJS

This is in a fairly early stage of development, so do not expect too much yet! It should be useable on Unix and MacOS, though I have only tried on Windows as that is all I have.

It is written in Python using Django, and is run as a web server. Once it is up and running, access it via your browser. Help files are included, and accessed from within it.

# Get QEditor

Firstly, you need QEditor. Click the "Code" button towards the top right of this page, and select download. The code will be downloaded as a ZIP file; you need to extract that into a convenient location.

# Install Python/Django

To run it you will need to download Python and Django. Download Python from here, if you do not already have it:
https://www.python.org/downloads/

Check it works by typing "python" at a command line. it should take you to an interactive session, and tell you the version. Type "exit()" to get out of that. Back at the command line, you should now be able to install Django:
```
python -m pip install Django
```
If that does not work, you may need to install PIP first - I have had people say this is the case on Linux. The following may do the trick, but I did not have to do it, so I am not sure.
```
wget https://bootstrap.pypa.io/get-pip.py
python ./get-pip.py
```
With Django installed, go to the folder you unzipped QEditor into, and then run it:
```
cd [whatever folder you unzipped into]
python manage.py runserver
```
Now open up yuour browser, and go to http://localhost:8000. You should see a welcome page, with a link to the editor. Click the link, and check it works okay.

# Install QuestJS

If you try to play the game, it will not work yet. You need to add the QuestJS files. These are not included as they get updated separately. If a new version of QuestJS comes out, this software does not get updated, but you can download the new version and install the files just the same

QuestJS can be found here:
https://github.com/ThePix/QuestJS/wiki

Click on the Code button (kind of middle-right), and select "Download Zip" from the drop-down, just as you did with QEDitor. Unzip the file, and then you need to copy across three folders - "assets", "lang" and "lib" - from there to the "edit/static/edit/" folder. You should then be able to play your game from the editor.

# Super-user

This is optional, but you can make yourself a superuser!
```
python manage.py createsuperuser
```
This will allow you to go to the database admin page. One possible reason to do that is to delete an item, another is to move an item out of a location that no longer exists. 


# To-Do List

Some areas for improvement

* Export facility, with versioning and options for play vs beta
* Better script support. Should be possible to check code if we know what the parameters are. Use Blockly?
* Responses (in the QuestJS sense) - used by ask/tell, reactions and other things
* Easy way to add custom attributes
* Better styling, including icons for links on home page
* Better testing, in particular for views.py
* Multiple game handling
* Use Push API (https://developer.mozilla.org/en-US/docs/Web/API/Push_API) and JSON/XMLHttp to update pages
* Import from Quest 5
* Import from QuestJS

    
