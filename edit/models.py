from django.db import models

from .quest_data import *
from .utils import *








class MetaPage(models.Model):
    name = models.CharField(max_length=12)
    alias = models.CharField(max_length=12)
    help_text = models.TextField(blank=True, null=True)
    help_link = models.CharField(max_length=20, blank=True, null=True)
    return_type = models.CharField(max_length=10, blank=True, null=True)
    params = models.CharField(max_length=20, blank=True, null=True)
    order = models.IntegerField(default=-1)
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
        for el in MetaPage.objects.filter(category=obj.category):
            if test_rules(obj, el):
                lst.append(el)
        return lst
        #lst = list(MetaPage.objects.filter(category=obj.category))
        #return list(filter(lambda x: test_rules(obj, x), lst))

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




class MetaAttr(models.Model):
    #   code, name,
    #   requires big widget, template or lambda for widget,
    #   lambda for conversion of data from string in HTTP POST
    #   template or lambda for writing to JavaScript file
    #   help text
    
    # Save data as a human-friendly string. This means that for a list we save the entry in the list or the name of the object, not the index
    TYPE_CHOICES =(
        ("id",  "id string",
            False, '<input type="text" value="*value*" name="*name*" id="name-input"/>',
            lambda x: x,
            '"*value*"',
            'Can only contain standard letters and numbers, plus underscore.',
        ),  # Must be present, and only present once; stored as an attribute rather than in a QAttr record
        
        ("str", "short string",
            False, '<input type="text" value="*value*" name="*name*"/>',
            lambda x: x,
            '"*value*"',
            '',
        ),
        
        ("txt", "text",         
            True, '<textarea rows="7" cols="120" name="*name*">*value*</textarea>',
            lambda x: x,
            '"*value*"',
            '',
        ),
        
        ("scr", "script",
            True, '<textarea rows="6" cols="40" name="*name*" style="background-color:#888;font-family:monospace">*value*</textarea>',        
            lambda x: x,
            'function() {*value*}',  # !!! May want to add params, etc
            '',
        ),

        ("say", "string array",
            True, '<textarea rows="7" cols="120" name="*name*">*value*</textarea>',
            lambda x: x,
            lambda x: string_array_to_js(x),
            'Enter each entry as part of a single string, using a vertical bar to separate.',
        ),  # !!!

        ("rgx", "regex",        
            False, '<input type="text" value="*value*" name="*name*"/>',
            lambda x: x,
            '/*value*/',
            'This is a regular expression.',
        ),

        ("int", "integer",
            False, lambda mattr, value: f'<input type="number" value="{value}" name="{mattr.name}"/>' if value else f'<input type="number" name="{mattr.name}"/>',
            lambda x: int(x) if x else None,
            '*value*',
            '',
        ),
        
        ("flt", "float",        
            False, lambda mattr, value: f'<input type="number" value="{value}" name="{mattr.name}"/>' if value else f'<input type="number" name="{mattr.name}"/>',
            lambda x: float(x) if x else None,
            '*value*',
            '',
        ),
        
        ("obj", "object",
            False, lambda mattr, value: select_choice(mattr.name, QObject.list_names('all'), value),
            lambda x: QObject.find_by_name(x),
            '"*value*"',
            '',
        ),

        ("itm", "item",          
            False, lambda mattr, value: select_choice(mattr.name, QObject.list_names('item'), value),
            lambda x: QObject.find_by_name(x),
            '"*value*"',
            '',
        ),

        ("loc", "location",     
            False, lambda mattr, value: select_choice(mattr.name, QObject.list_names('room'), value),
            lambda x: QObject.find_by_name(x),
            '"*value*"',
            '',
        ),

        ("chc", "choice",       
            False, lambda mattr, value: select_choice(mattr.name, mattr.options, value),
            lambda x: x,
            '"*value*"',
            '',
        ),

        ("gdr", "gender",       
            False, lambda mattr, value: select_choice(mattr.name, GENDER_OPTIONS, value),
            lambda x: x,
            #lambda x: 'pronouns.' + GENDER_OPTIONS[int(x)][0],
            'lang.pronouns.*value*',
            '',
        ),

        ("dir", "direction",    
            False, lambda mattr, value: select_choice(mattr.name, DIRECTIONS, value),
            lambda x: x,
            '"*value*"',
            '',
        ),

        ("cbx", "boolean flag", 
            False, lambda mattr, value: f'<input type="checkbox" name="{mattr.name}" checked/>' if value else  f'<input type="checkbox" name="{mattr.name}"/>',
            lambda x: x == 'True',
            lambda x: 'true' if x else 'false',
            '',
        ),
                
        ("btn", "button",        # a button sets or unsets an attribute, and then saves; use for templates as they change the buttons on the top
            False, lambda mattr, value: f'Set<input type="hidden" name={mattr.name} value="yes" />' if value else '<input type="button" value="Add" onclick="template_button(\'' + mattr.name + '\')"/>',
            lambda x: x == 'True',
            lambda x: 'true' if x else 'false',
            '',
        ),  

        # exits are complicated as they contain lots of attributes themselves
        # do we do them as objects?
        # or as complex attributes?
        # attributes:
        #    destination (or nowhere)
        #    exit_type (Exit, Link, NonExit, BarredExit, WayIn (item), WayOut, ClimbExit(item) u/d, StairsUp(item) card, StrairsDown(item) card
        #    script (simpleUse)
        #    msg
        #    npcLeaveMsg
        #    npcEnterMsg
        #    msgNPC
        #    hidden/locked/lit
        #    lockedMsg
        #    scenery
        #    alsoDir
        ("ext", "exit",       
            False, 'To be implemented!',
            lambda x: x.name,
            '"*value*"',
            '',
        ),
    )


    name = models.CharField(max_length=20)
    display_name = models.CharField(max_length=20)
    page = models.ForeignKey(MetaPage, on_delete=models.CASCADE)    
    order = models.IntegerField(default=-1)
    advanced = models.BooleanField(default=False)
    attr_type = models.CharField(max_length=3)
    help_text = models.TextField()
    category = models.CharField(max_length=4, default='item')  # item, room, sttg, game, opts
    rules = models.TextField()
    
    def __str__(self):
        return self.name
        
    def get_type(self):
        return next(x for x in MetaAttr.TYPE_CHOICES if x[0] == self.attr_type)

    # Convert the given value to the appropriate type. Eg if the attr_type is a cbx, it will
    # be converted to a Boolean. Uses lambdas in the array to do this.
    def to_type(self, value):
        # Unit tested
        t = self.get_type()
        return t[4](value)
        
    def get_help_text(self):
        # Unit tested
        return self.help_text + ' ' + self.get_type()[6]
        
        
    # Find the MetaAttr with the given data
    @staticmethod
    def get(name, category):
        try:
            return MetaAttr.objects.get(name=name, category=category)
        except MetaAttr.DoesNotExist as exc:
            raise RuntimeError(f"Failed to find MetaAttr with name={name} category={category}") from exc





class QObject(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=4, default='item')  # item, room or sttg

    def __str__(self):
        return self.name
        
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


    # Get an attribute for this object
    # It will be converted to the correct type,
    # despite being stored in the database as a string
    def get_attr(self, name):
        # Unit tested
        if name == 'name':
            return self.name
            
        else:
            attr = MetaAttr.get(name=name, category=self.category)
            original_set = QAttr.objects.filter(attr=attr, qobject=self)
            if original_set.count() == 0:
                return None
            elif original_set.count() == 1:
                return attr.to_type(original_set.first().value)
            else:
                raise RuntimeError('Found multiple attributes for ' + self.name + ' and ' + attr.name)
                
    # Returns a string; this object in JS code
    def to_js(self):
        # Unit tested
        if self.category == 'sttg':
            s = ''
        
        else:
            s = 'createRoom("' if self.category == 'room' else 'createItem("'
            s += self.name + '", '
            for template in self.list_templates():
                s += template + '(), '
            s += '{\n'

        attrs = QAttr.objects.filter(qobject=self)
        for attr in attrs:
            s += attr.to_js()
                
                
        if self.category != 'sttg':
            s += '})\n\n'
        return s
        
    # Get a string list of templates for te item.
    def list_templates(self):
        if self.category != 'item':
            return []
            
        lst = []
        mattrs = MetaPage.get(self, 'templates').metaattr_set.all()
        for attr in mattrs:
            if self.get_attr(attr.name):
                lst.append(attr.name.upper())
        return lst
        


    # Updates attributes of the object. Used by the view.
    def update(self, data, page):
        # Unit tested
        mattrs = MetaAttr.objects.filter(page=page, category=self.category)
        for attr in mattrs:
            value = None
            if attr.attr_type == 'cbx' or  attr.attr_type == 'btn':
                value = attr.name in data
                
            else:
                value = data[attr.name]
            self.set_attr(attr.name, value)



    @staticmethod
    def find_by_name(name):
        # Unit tested
        original_set = QObject.objects.filter(name=name)
        if original_set.count() == 0:
            return None
        elif original_set.count() == 1:
            return original_set.first()
        else:
            raise RuntimeError('Found multiple objects with name ' + name)


    @staticmethod
    def list_names(option):
        # Unit tested
        if option == 'all':
            return [q.name for q in QObject.objects.all().order_by('name')]
        else:
            return [q.name for q in QObject.objects.filter(category=option).order_by('name')]
            

    # Returns a string; every item and location in JS code
    @staticmethod
    def get_js():
        code = ''
        for o in QObject.objects.all().order_by('name'):
            if o.category == 'item' or o.category == 'room':
                code += o.to_js()
        return code


    # Returns a string; the settings in JS code
    @staticmethod
    def get_settings_js():
        code = ''
        o = QObject.objects.get(category='sttg')
        return o.to_js()


          



class QAttr(models.Model):
    value = models.TextField()

    attr = models.ForeignKey(MetaAttr, on_delete=models.CASCADE)
    qobject = models.ForeignKey(QObject, on_delete=models.CASCADE)

    # Returns a string; this attribute in JS code
    def to_js(self):
        if not self.value and self.value != 0:
            return ''
            
        # Unit tested
        attr_type = self.attr.get_type()
        
        if self.attr.category == 'sttg':
            s = 'settings.' + self.attr.name + ' = '
        else:
            s = '  ' + self.attr.name + ':'
            
        if isinstance(attr_type[5], str):
            s += attr_type[5].replace('*value*', str(self.value))
        else:
            s += attr_type[5](self.value)

        if self.attr.category == 'sttg':
            s += '\n'
        else:
            s += ',\n'
        return s




def kick_start():
    # Unit tested
    MetaPage.objects.all().delete()
    MetaAttr.objects.all().delete()
    QObject.objects.all().delete()
    QAttr.objects.all().delete()

    for idx, key in enumerate(META_ATTRS):
        meta = META_ATTRS[key]
        page = MetaPage.objects.create(name=key, alias=meta['alias'], category=meta['category'], order=idx)
        for key in ['help_link', 'rules', 'home']:
            if key in meta:
                setattr(page, key, meta[key])
        page.save()
            
        for data in meta['attrs']:
            #print((f"MetaAttr with name={data[0]} category={meta['category']}"))
            mattr = MetaAttr.objects.create(
                page=page, category=meta['category'],
                name=data[0], display_name=data[1],
                advanced=data[2], attr_type=data[3], rules=data[4], help_text=data[5])
            if len(data) == 8:
                setattr(mattr, 'return_type', data[6])
                setattr(mattr, 'params', data[7])
                mattr.save()
            

    o = QObject.objects.create(name='settings', category='sttg')
    for data in INIT_OBJECTS:
        o = QObject.objects.create(
            name=data[0], category='room' if data[1] else 'item')
            
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
            