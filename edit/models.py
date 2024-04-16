from django.db import models

from .quest_data import *
from .utils import *
from django.utils.html import mark_safe



VERSION = '0.1'



# An object can be edited via a number of pages (or tabs?) within a web page.
# A page has a category - pages for rooms will only get shown for a room
# There should be one and only one "home" page for each category
# Every MetaAttr belongs to a page
class MetaPage(models.Model):
    name = models.CharField(max_length=12)
    alias = models.CharField(max_length=12)
    help_text = models.TextField(blank=True, null=True)
    help_link = models.CharField(max_length=20, blank=True, null=True)
    #order = models.IntegerField(default=-1)
    category = models.CharField(max_length=4, default='item')  # item, room or sttg
    rules = models.TextField()
    home = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # Get all the pages that match the category of the given object
    @staticmethod
    def get_all(obj):
        # Unit tested
        return MetaPage.objects.filter(category=obj.category)

    # Get all the pages that match the category and rules for the given object
    @staticmethod
    def get_some(obj):
        lst = []
        settings = obj.qgame.get_settings()
        for el in MetaPage.objects.filter(category=obj.category):
            if test_rules(obj, settings, el):
                lst.append(el)
        return lst

    # Get the home page for this object
    @staticmethod
    def get_home(obj):
        return MetaPage.objects.get(home=True, category=obj.category)

    # Get the names page for this object
    @staticmethod
    def get(obj, name):
        try:
            return MetaPage.objects.get(name=name, category=obj.category)
        except MetaPage.DoesNotExist as exc:
            raise RuntimeError(f"Failed to find MetaPage with name={name} category={obj.category}") from exc



# Every MetaAttr has a ttpe - a MetaAttrType
# This cannot be a database model, as it stores lambdas, so the various types are defined in MetaAttr.TYPE_CHOICES
# The type handles how values are converted to and from string, and how they are displayed on the web page.
class MetaAttrType():
    def __init__(self, code, name, widget, default = '', big_widget = False, from_db = None, from_http = None, to_js = None, help_text = None, ignore_for_js = False):
        self.code = code
        self.name = name
        self.widget = widget
        self.default = default
        self.big_widget = big_widget
        self.from_db = from_db if from_db else lambda x, attr:x
        self.from_http = from_http if from_http else lambda x, attr:x if x else ''
        self.to_js = to_js if to_js else '"*value*"'
        self.help_text = help_text
        self.ignore_for_js = ignore_for_js

    def __str__(self):
        return 'MetaAttrType[' + self.name + ']'




class MetaObjectAttrType(MetaAttrType):
    def __init__(self, code, name, category):
        super().__init__(code, name,
          lambda mattr, value, obj: select_choice(mattr.name, obj.qgame.list_names(self.category), value),
          from_db = lambda x, attr: attr.qobject.qgame.find_by_name(x),
          from_http = lambda x, attr: attr.qobject.qgame.find_by_name(x),
        )
        self.category = category

    def __str__(self):
        return 'MetaObjectAttrType[' + self.name + ']'





# MetaAttr objects define the attributes available
# An item has an "alias" attribute. The details of what an alias attribute is
# (as opposed to the actual value) is in the MetaAttr.
# A MetaAttr belongs to a MetaPage, determining which tab it is shown on.
# It has a category, which should match that of the MetaPage
class MetaAttr(models.Model):
    #   lambda for conversion of data from string in HTTP POST or None if not saved to database
    #   template or lambda for writing to JavaScript file
    #   help text
    
    # Save data as a human-friendly string. This means that for a list we save the entry in the list or the name of the object, not the index
    TYPE_CHOICES =(

        # String attribute types - all pretty straightforward
        # Must be present, and only present once; stored as an attribute rather than in a QAttr record
        MetaAttrType("id",  "id string", '<input type="text" value="*value*" name="*name*" class="restricted-input"/>',
            help_text='Can only contain standard letters and numbers, plus underscore.',
        ),  
        MetaAttrType("str", "short string", '<input type="text" value="*value*" name="*name*"/>',
        ),
        MetaAttrType("nst", "short string, not editable", lambda mattr, value, obj: value,
        ),
        MetaAttrType("txt", "text", '<textarea rows="7" cols="120" name="*name*">*value*</textarea>',
            big_widget=True,
        ),
        MetaAttrType("imp", "implemetation notes", '<textarea rows="7" cols="120" name="*name*">*value*</textarea>',
            big_widget=True,
            ignore_for_js=True,
            help_text='Use to note what you still have to do or what you did it this way. This will not be part of your published game.',
        ),

        
        # Number attribute types - fairly straightforward, just need convertingh to from string for database
        MetaAttrType("int", "integer", lambda mattr, value, obj: f'<input type="number" value="{value}" name="{mattr.name}"/>' if value else f'<input type="number" name="{mattr.name}"/>',
            from_db=lambda x, attr: int(x) if x else 0,
            from_http=lambda x, attr: int(x) if x else 0,
            to_js='*value*',
            default=0,
        ),
        MetaAttrType("flt", "float", lambda mattr, value, obj: f'<input type="number" value="{value}" name="{mattr.name}"/>' if value else f'<input type="number" name="{mattr.name}"/>',
            from_db=lambda x, attr: float(x) if x else 0.0,
            from_http=lambda x, attr: float(x) if x else None,
            to_js='*value*',
        ),
        
        
        # Object attribute types - all pretty straightforward, just save object name as string
        # Note for JS save the name as a string (object may not exist yet)
        MetaObjectAttrType("obj", "location", 'all'),
        MetaObjectAttrType("rgn", "location", 'regn'),
        MetaObjectAttrType("itm", "location", 'item'),
        MetaObjectAttrType("loc", "location", 'room'),



        # Selection attribute types - save selection as string, not index
        # The only difference to a string is the widget
        # A choice is one of a set of options, so requires extra parameter when setting up, either list or dictionary
        MetaAttrType("chc", "choice", lambda mattr, value, obj: select_choice(mattr.name, mattr.options(), value),
        ),
        # Pre-defined options
        MetaAttrType("gdr", "gender", lambda mattr, value, obj: select_choice(mattr.name, GENDER_OPTIONS, value),
            to_js='lang.pronouns.*value*',
        ),
        MetaAttrType("dir", "direction", lambda mattr, value, obj: select_choice(mattr.name, DIRECTIONS, value),
        ),


        # Boolean attribute types - save as True or False in database
        # HTTP handles this by whether the attribute is present or not, which is an issue
        MetaAttrType("cbx", "boolean flag", lambda mattr, value, obj: f'<input type="checkbox" name="{mattr.name}" checked/>' if value else  f'<input type="checkbox" name="{mattr.name}"/>',
            from_db=lambda x, attr: x == 'True',
            from_http=lambda x, attr: x == 'True',
            to_js=lambda x: 'true' if x else 'false',
            default=False,
        ),
        # A button sets (or unsets?) an attribute, and then saves; use for templates as they change the buttons on the top
        MetaAttrType("btn", "button", lambda mattr, value, obj: f'Set<input type="hidden" name={mattr.name} value="yes" />' if value else '<input type="button" value="Add" onclick="template_button(\'' + mattr.name + '\')"/>',
            from_http=lambda x, attr: x == 'True',
            to_js=lambda x: 'true' if x else 'false',
        ),  


        # Script
        # Some work to do here!!! Need the to_js to handle parameters and maybe return
        MetaAttrType("scr", "script", '<textarea rows="6" cols="40" name="*name*" style="background-color:#888;font-family:monospace">*value*</textarea>',        
            big_widget=True,
            to_js='function() {*value*}',  # !!! May want to add params, etc
        ),
        

        # String array
        MetaAttrType("say", "string array", '<textarea rows="7" cols="120" name="*name*">*value*</textarea>',
            big_widget=True,
            to_js=lambda x: string_array_to_js(x, '\n'),
            help_text='Enter each entry on its own line.',
        ),


        # Regular expression
        MetaAttrType("rgx", "regex", '<input type="text" value="*value*" name="*name*"/>',
            to_js='/*value*/',
            help_text='This is a regular expression.',
        ),


        # Special; uses get_special_widget to get the HTML widget, but otherwise as per string
        MetaAttrType("spc", "special", lambda mattr, value, obj: obj.get_special_widget(mattr.name),
            to_js=lambda x: '',
        ),

        # Links
        MetaAttrType("lnk", "link", lambda mattr, value, obj: obj.get_link_widget(mattr),
            big_widget=True,
        ),    
        
        # Exits
        MetaAttrType("ext", "exit", lambda mattr, value, obj: obj.get_special_widget(mattr.name),
            ignore_for_js=True,
        ),
            
                
        # Null; no widget, but appears as comment
        MetaAttrType("nul", "Not a proper attribute", '',
            ignore_for_js=True,
        ),
    )


    name = models.CharField(max_length=20)
    display_name = models.CharField(max_length=20)
    page = models.ForeignKey(MetaPage, on_delete=models.CASCADE)    
    advanced = models.BooleanField(default=False)
    attr_type = models.CharField(max_length=3)
    help_text = models.TextField()
    category = models.CharField(max_length=4, default='item')  # item, room, sttg, game, exit, regn
    rules = models.TextField()
    options_as_string = models.TextField(default='')
    return_type= models.CharField(max_length=12, blank=True, null=True)
    params = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return 'MetaAttr("' + self.name + '")'
        
        
    # Gets the associated MetaAttrType
    def get_type(self):
        try:
            return next(x for x in MetaAttr.TYPE_CHOICES if x.code == self.attr_type)
        except StopIteration as exc:
            raise RuntimeError('Failed to find self.attr_type=' + self.attr_type) from exc
    

    # Convert the given value to the appropriate type. Eg if the attr_type is a cbx, it will
    # be converted to a Boolean. Uses lambdas in the array to do this.
    def to_type(self, attr):
        # Unit tested
        value = attr.value
        t = self.get_type()
        #print(value)
        return t.from_db(value, attr)
    
    
    def get_help_text(self):
        # Unit tested
        s = self.help_text
        if self.get_type().help_text:
            s += ' ' + self.get_type().help_text
        return s
        
    # For a chc type MetaAttr, gets an array of options
    # Not currently used
    def options(self):
        return self.options_as_string.split('\n')
        
        
    # Find the MetaAttr with the given data
    # Raised an error if it does not exist
    @staticmethod
    def get(name, category):
        try:
            return MetaAttr.objects.get(name=name, category=category)
        except MetaAttr.DoesNotExist as exc:
            raise RuntimeError(f"Failed to find MetaAttr with name={name} category={category}") from exc



# Currently multiple games are not supported, but they may well be in the future
# To facilitate that, every object belongs to a game object.
# Also handles version tracking
class QGame(models.Model):
    name = models.CharField(max_length=50)
    version = models.IntegerField()
    subversion = models.IntegerField()

    def __str__(self):
        return 'QGame("' + self.name + '")'

    def get_version(self):
        return str(self.version) + '.' + str(self.subversion)


    # Returns a string; the objects in JS code (data.js)
    def to_data_js(self):
        code = '"use strict"\n\n'
        for o in self.qobject_set.filter(qgame=self).all():
            code += o.to_js()
        return code

    def get_settings(self):
        return self.find_by_name('settings')
    

    # Returns a string; the settings in JS code (settings.js)
    def to_settings_js(self):
        code = '"use strict"\n\n'
        o = self.get_settings()
        return o.to_js()

    def find_by_name(self, name):
        # Unit tested
        original_set = QObject.objects.filter(qgame=self, name=name)
        if original_set.count() == 0:
            return None
        elif original_set.count() == 1:
            return original_set.first()
        else:
            raise RuntimeError('Found multiple objects with name ' + name)

    def list_names(self, option):
        # Unit tested
        if option == 'all':
            return [q.name for q in QObject.objects.filter(qgame=self).order_by('name')]
        else:
            return [q.name for q in QObject.objects.filter(qgame=self, category=option).order_by('name')]
 
    def list(self, option):
        if option == 'all':
            return QObject.objects.filter(qgame=self).order_by('name')
        else:
            return QObject.objects.filter(qgame=self, category=option).order_by('name')

    # Return a list of items that have no location set
    def get_by_attr(self, category, attr_name, value):
        mattr = MetaAttr.objects.get(category=category, name=attr_name)
        lst = []
        for qattr in QAttr.objects.filter(qobject__qgame=self, attr=mattr, value=value):
            lst.append(qattr.qobject)
        return lst

    # Return a list of items that do not have the given attribute
    def get_not_attr(self, category, attr_name):
        mattr = MetaAttr.objects.get(category=category, name=attr_name)
        all_objs = QObject.objects.filter(qgame=self, category=category).order_by('name')
        
        exclude = []
        for qattr in QAttr.objects.filter(attr=mattr):
            exclude.append(qattr.qobject)
        return [x for x in all_objs if x not in exclude]
          
    # Returns a list of duplicated names
    def get_duplicates(self):
        #print('here')
        names = self.list_names('all')
        seen = set()
        seen_add = seen.add
        # adds all elements it doesn't know yet to seen and all other to seen_twice
        seen_twice = set( x for x in names if x in seen or seen_add(x) )
        # turn the set into a list (as requested)
        return list(seen_twice)





# An object in the game; either an item or a location (room)
# Also used to store exits and settings
class QObject(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=4, default='item')  # item, room or sttg
    qgame = models.ForeignKey(QGame, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
        
    # Used on the HTML page for the item
    def title_name(self):
        if self.category == 'exit':
            return 'Exit ' + self.get_attr('direction') + ' from ' + self.get_attr('loc').name + ' to ' + self.get_attr('destination').name
        return self.name
        
    # A full print out of the item with all attributes
    def print(self):
        s = self.name + ': '
        attrs = QAttr.objects.filter(qobject=self)
        for attr in attrs:
            s += attr.attr.name + '=' + str(self.get_attr(attr.attr.name)) + '; '
        return s
        
    def display_name(self):
        s = self.name
        alias = self.get_attr('alias')
        if alias:
            s += ' ("' + alias + '")'
        return s
       
    def create_object_link(self, mattr, data):
        if self == 'name':
            raise ValueError("Trying to create link from an item to itself")
        
        #attrs = QAttr.objects.filter(qobject=data)
        #attr = MetaAttr.get(name=attr.attr.name, category='item')
        
        obj = QObject.objects.get(name=data[0])
        try:
            attr = MetaAttr.objects.get(name=data[0], category=obj.category)
        except MetaAttr.DoesNotExist as exc:
            raise RuntimeError(f"Failed to find MetaAttr with name={data["name"]} category={obj.category}") from exc

        ItemToItemLinks.objects.create(primaryobject=self, secondaryobject=attr, success=True, response="Oh my a hat", link_type='give')


    
    # Create an exit from this location to the given destination and also the reverse
    # Currently only used in one test
    def create_link(self, dest, dr):
        if self == dest:
            raise ValueError("Trying to create link from a location to itself")
        ext2 = dest.create_exit(self, reverse_dir(dr))
        ext1 = self.create_exit(dest, dr)
        return  ext1, ext2

    # Create an exit from this location to the given destination
    def create_exit(self, dest, dr, exit_type = 'Simple'):
        ext = QObject.objects.create(name='__exit_' + self.name + '_' + dr, category='exit', qgame=self.qgame)
        ext.set_attr('loc', self)
        ext.set_attr('destination', dest)
        ext.set_attr('direction', dr)
        ext.set_attr('exit_type', exit_type)
        return ext
      
    # Find an exit from this location in the given direction, or None if none
    def find_exit(self, dr):
        name = '__exit_' + self.name + '_' + dr
        exts = QObject.objects.filter(name=name, category='exit')
        if exts.count() == 0:
            return None
        if exts.count() == 1:
            return exts[0]
        raise ValueError("To many exits found going " + dr + " from " + self.name)            
        
    # Set an attribute for this object
    def set_attr(self, name, value):
        # Unit tested
        if name == 'name':
            self.name = value
            self.save()
            return None
            
        else:
            attr = MetaAttr.get(name=name, category=self.category)
                
            original_set = QAttr.objects.filter(attr=attr, qobject=self)
            if original_set.count() == 0:
                if value == None:
                    return None
                return QAttr.objects.create(attr=attr, qobject=self, value=value)
            elif original_set.count() == 1:
                if value == None:
                    original_set.delete()
                    return None
                qa = original_set.first()
                qa.value = value
                qa.save()
                return qa
            else:
                raise RuntimeError('Found multiple attributes for ' + self.name + ' and ' + attr.name)

    # Get an attribute for this object as a string, or None
    def get_attr_as_s(self, name):
        # Unit tested
        if name == 'name':
            return self.name
            
        else:
            attr = MetaAttr.get(name=name, category=self.category)
            if not hasattr(attr.get_type(), "from_db"):
                return None

            original_set = QAttr.objects.filter(attr=attr, qobject=self)
            if original_set.count() == 0:
                return str(attr.get_type().default)
            elif original_set.count() == 1:
                return original_set.first().value
            else:
                raise RuntimeError('Found multiple attributes for ' + self.name + ' and ' + attr.name)
                
    # Get an attribute for this object
    # It will be converted to the correct type,
    # despite being stored in the database as a string
    def get_attr(self, name):
        # Unit tested
        if name == 'name':
            return self.name
            
        else:
            attr = MetaAttr.get(name=name, category=self.category)
            if not hasattr(attr.get_type(), "from_db"):
                return None

            original_set = QAttr.objects.filter(attr=attr, qobject=self)
            if original_set.count() == 0:
                return attr.get_type().default
            elif original_set.count() == 1:
                return original_set.first().get_value()
            else:
                raise RuntimeError('Found multiple attributes for ' + self.name + ' and ' + attr.name)
                
    # Returns a string; this object in JS code
    def to_js(self):
        # Unit tested
        
        if self.category not in ('sttg', 'room', 'item'):
            return ''
            
        if self.category == 'sttg':
            s = 'settings.version = "' + self.qgame.get_version() + '"\n'
        
        else:
            s = 'createRoom("' if self.category == 'room' else 'createItem("'
            s += self.name + '", '
            for template in self.list_templates():
                s += template + '(), '
            s += '{\n'

        # attributes
        attrs = QAttr.objects.filter(qobject=self)
        for attr in attrs:
            s += attr.to_js()

        # exits
        if self.category == 'room':
            exits = self.get_contents(category='exit')
            for e in exits:
                s += e.exit_to_js()

        if self.category != 'sttg':
            s += '})\n\n'
        return s
        
    # Returns a string; this exit in JS code as an attribute of a location
    def exit_to_js(self):
        
        if self.category != 'exit':
            return ''
            
        s = '  ' + self.get_attr('direction') + ':new '
        if self.get_attr('exit_type') == 'Simple':
            # north:new Exit("lounge"),
            s += 'Exit("' + self.get_attr_as_s('destination') + '"),\n'
        else:
            # north:new Exit("lounge", {\n}),
            s += self.get_attr('exit_type') + '("' + self.get_attr_as_s('destination') + '", {\n'

            attrs = QAttr.objects.filter(qobject=self)
            for attr in attrs:
                if attr.attr.name not in ('loc', 'direction', 'destination', 'exit_type'):
                    s += attr.to_js('    ')
                
            s += '  }),\n'
        return s
        
    # Get a string list of templates for the item.
    def list_templates(self):
        if self.category != 'item':
            return []
            
        lst = []
        mattrs = MetaPage.get(self, 'templates').metaattr_set.all()
        for attr in mattrs:
            if self.get_attr(attr.name):
                lst.append(attr.name.upper())
        return lst

    # Get a list of attributes of the given type for this object
    # Used by get_contents.
    def _get_contents_attrs(self, attr_name, category):
        loc_attr = MetaAttr.get(attr_name, category)
        return QAttr.objects.filter(attr=loc_attr, value=self.name)

    # Get an object list of items that have this as the location
    def get_contents(self, attr_name='loc', category='item'):
        lst = []
        for qattr in self._get_contents_attrs(attr_name, category):
            lst.append(qattr.qobject)
        return lst

    # Returns True if the object contains at least one item
    def has_contents(self, attr_name='loc'):
        return len(self.get_contents(attr_name)) > 0

    # get_contents for a region
    def room_list(self):
        return self.get_contents('region', 'room')

    # Updates attributes of the object. Used by the view.
    def update(self, data, page):
        # Unit tested
        mattrs = MetaAttr.objects.filter(page=page, category=self.category)
        for attr in mattrs:
            #if not attr.get_type().from_db:
            #    continue

            if attr.attr_type != 'nob' and  attr.attr_type != 'nst':
                value = None
                if attr.attr_type == 'cbx' or  attr.attr_type == 'btn':
                    value = attr.name in data
                    self.set_attr(attr.name, value)
                
                elif attr.attr_type == 'lnk':
                    self.create_object_link(attr, data)     
                    
                elif attr.name in data:
                    value = data[attr.name]
                    self.set_attr(attr.name, value)

    def get_special_widget(self, name):
        if name == 'item-list':
            s = '<ul>'
            for o in self.get_contents():
                s += '<li><a href="/edit/object/' + str(o.id) + '" target="_blank">' + o.display_name() + '</a></li>'
        
        
            s += '</ul>'
            s += '<input type="text" id="add-item-' + self.name + '" class="restricted-input"/> [<span class="clickable" onclick="add_obj(\'item\', \'' + self.name + '\')">Add</span>]'
            return s

        if name == 'exits':
            s = '<table><tr>'
            s += exit_td(self, 'northwest')
            s += exit_td(self, 'north')
            s += exit_td(self, 'northeast')
            s += exit_td(self, 'in')
            s += exit_td(self, 'up')
            s += '</tr><tr>'
            s += exit_td(self, 'west')
            s += '<td></td>'
            s += exit_td(self, 'east')
            s += exit_td(self, 'out')
            s += exit_td(self, 'down')
            s += '</tr><tr>'
            s += exit_td(self, 'southwest')
            s += exit_td(self, 'south')
            s += exit_td(self, 'southeast')
            s += '<td colspan="2"></td>'
            s += '</tr><tr>'
            s += '</table>'
            
            options = self.qgame.list_names('room')
            s += '<br/>New exit to: '
            s += select_choice('destination', options, None)
            s += '<br/><input type="checkbox" id="exit-is-link"/>Exit in reverse direction too?'
        
            #s = '<input type="text" id="add-item-' + self.name + '"/> [<span class="clickable" onclick="add_obj(\'item\', \'' + self.name + '\')">Add</span>]'

            #META_ATTRS['room']['exitsRoom']['attrs'].append((dr, f'Go {dr} exit.', True, 'ext',  '', 'An exit in the selected direction.'))
            
            
            return s

        return 'Unrecognised list type: ' + name
    
    def get_link_widget(self, mattr):
        s = '<ul>'
        for o in self.get_contents():
            s += '<li><a href="/edit/object/' + str(o.id) + '" target="_blank">' + o.display_name() + '</a></li>'
    
        options = self.qgame.list_names('item')
        s += '</ul>'
        s += select_choice('giveitems', options, None)
        s += '<input type="checkbox" id="success"/>Success?'
        s += '<br/><textarea rows="7" cols="120" name="response">*Response*</textarea>'
        return mark_safe(s)

        

            
    # Do this as a property so Django templates can use it
    @property
    def expanded(self):
        return self.get_attr('expanded')

    
            



class QAttr(models.Model):
    value = models.TextField()

    attr = models.ForeignKey(MetaAttr, on_delete=models.CASCADE)
    qobject = models.ForeignKey(QObject, on_delete=models.CASCADE)

    def __str__(self):
        return self.qobject.name + '->' + self.attr.name + ' = ' + self.value
        
    # use the property value to get the value as it is stored in the database, a string
    # use this to get it as the correct type
    def get_value(self):
        return self.attr.to_type(self)
        
        

    # Returns a string; this attribute in JS code
    def to_js(self, indent = '  '):
        if not self.value and self.value != 0:
            return ''
            
        # Unit tested
        attr_type = self.attr.get_type()
        if attr_type.ignore_for_js:
            return ''
        
        if self.attr.category == 'sttg':
            s = 'settings.' + self.attr.name + ' = '
        else:
            s = indent + self.attr.name + ':'
            
        if isinstance(attr_type.to_js, str):
            s += attr_type.to_js.replace('*value*', str(self.value))
        elif attr_type.to_js:
            s += attr_type.to_js(self.value)

        if self.attr.category == 'sttg':
            s += '\n'
        else:
            s += ',\n'
        return s




def kick_start():
    # Unit tested
    QGame.objects.all().delete()
    MetaPage.objects.all().delete()
    MetaAttr.objects.all().delete()
    QObject.objects.all().delete()
    QAttr.objects.all().delete()
    
    qgame = QGame.objects.create(name='example', version=0, subversion=1)

    for cat in META_ATTRS:
        for key in META_ATTRS[cat]:
            meta = META_ATTRS[cat][key]
            page = MetaPage.objects.create(name=key, alias=meta['alias'], category=cat)
            for key in ['help_link', 'rules', 'home']:
                if key in meta:
                    setattr(page, key, meta[key])
            page.save()
                
            for data in meta['attrs']:
                #print((f"MetaAttr with name={data[0]} category={meta['category']}"))
                mattr = MetaAttr.objects.create(
                    page=page, category=cat,
                    name=data[0], display_name=data[1],
                    advanced=data[2], attr_type=data[3], rules=data[4], help_text=data[5])
                if mattr.attr_type == 'scr':
                    setattr(mattr, 'return_type', data[6])
                    setattr(mattr, 'params', data[7])
                    mattr.save()
                if mattr.attr_type == 'chc':
                    l = []
                    if isinstance(data[6], list):
                        for x in data[6]:
                            l.append(x + ':' + x)
                    else:
                        for k, v in data[6].items():
                            l.append(k + ':' + v)
                    setattr(mattr, 'options_as_string', '|'.join(l))
                    mattr.save()
            

    o = QObject.objects.create(name='settings', category='sttg', qgame=qgame)
    for data in INIT_OBJECTS:
        o = QObject.objects.create(name=data[0], category=data[1], qgame=qgame)

    for data in INIT_EXITS:
        from_room = qgame.find_by_name(data[1])
        to_room = qgame.find_by_name(data[2])
        ext = from_room.create_exit(to_room, data[3], data[0])
        if len(data) == 5:
            ext.set_attr('msg', data[4])
            
    for data in INIT_ATTRS:
        obj = QObject.objects.get(name=data[0])
        try:
            attr = MetaAttr.objects.get(name=data[1], category=obj.category)
        except MetaAttr.DoesNotExist as exc:
            raise RuntimeError(f"Failed to find MetaAttr with name={data[1]} category={obj.category}") from exc

        QAttr.objects.create(
            qobject=obj,
            attr=attr,
            value=data[2]
        )
        
            
class ItemToItemLinks(models.Model):

    primaryobject = models.ForeignKey(QObject, on_delete=models.CASCADE, related_name='PrimaryKey')
    secondaryobject = models.ForeignKey(QObject, on_delete=models.CASCADE, related_name='SecondaryKey')    
    success = models.BooleanField(default=False)
    response = models.TextField()
    link_type = models.CharField(max_length=12, default=None)
    

    def get_value(self):
        return self.attr.to_type(self)
