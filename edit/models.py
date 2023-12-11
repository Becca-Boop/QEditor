from django.db import models

from .quest_data import *
from .utils import *


VERSION = 1





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
        settings = QObject.get_settings()
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



# cannot be a database model, as it stores lambdas
class MetaAttrType():
    def __init__(self, code, name, widget, default = '', big_widget = False, from_db = None, from_http = None, to_js = None, help_text = None):
        self.code = code
        self.name = name
        self.widget = widget
        self.default = default
        self.big_widget = big_widget
        self.from_db = from_db if from_db else lambda x:x
        self.from_http = from_http
        self.to_js = to_js
        self.help_text = help_text

    def __str__(self):
        return 'MetaAttrType[' + self.name + ']'




class MetaAttr(models.Model):
    #   lambda for conversion of data from string in HTTP POST or None if not saved to database
    #   template or lambda for writing to JavaScript file
    #   help text
    
    # Save data as a human-friendly string. This means that for a list we save the entry in the list or the name of the object, not the index
    TYPE_CHOICES =(

        # Must be present, and only present once; stored as an attribute rather than in a QAttr record
        MetaAttrType("id",  "id string", '<input type="text" value="*value*" name="*name*" class="restricted-input"/>',
            from_http=lambda x: x,
            to_js='"*value*"',
            help_text='Can only contain standard letters and numbers, plus underscore.',
        ),  
        
        MetaAttrType("str", "short string", '<input type="text" value="*value*" name="*name*"/>',
            from_http=lambda x: '' if not x else x,
            to_js='"*value*"',
        ),
        
        MetaAttrType("nst", "short string, not editable", lambda mattr, value, obj: value,
            from_http=lambda x: '' if not x else x,
            to_js='"*value*"',
        ),
        
        MetaAttrType("txt", "text", '<textarea rows="7" cols="120" name="*name*">*value*</textarea>',
            big_widget=True,
            from_http=lambda x: '' if not x else x,
            to_js='"*value*"',
        ),
        
        MetaAttrType("scr", "script", '<textarea rows="6" cols="40" name="*name*" style="background-color:#888;font-family:monospace">*value*</textarea>',        
            big_widget=True,
            from_http=lambda x: '' if not x else x,
            to_js='function() {*value*}',  # !!! May want to add params, etc
        ),

        MetaAttrType("say", "string array", '<textarea rows="7" cols="120" name="*name*">*value*</textarea>',
            big_widget=True,
            from_http=lambda x: '' if not x else x,
            to_js=lambda x: string_array_to_js(x),
            help_text='Enter each entry as part of a single string, using a vertical bar to separate.',
        ),  # !!!

        MetaAttrType("rgx", "regex", '<input type="text" value="*value*" name="*name*"/>',
            from_http=lambda x: '' if not x else x,
            to_js='/*value*/',
            help_text='This is a regular expression.',
        ),

        MetaAttrType("int", "integer", lambda mattr, value, obj: f'<input type="number" value="{value}" name="{mattr.name}"/>' if value else f'<input type="number" name="{mattr.name}"/>',
            from_db=lambda x: int(x) if x else 0,
            from_http=lambda x: int(x) if x else 0,
            to_js='*value*',
            default=0,
        ),
        
        MetaAttrType("flt", "float", lambda mattr, value, obj: f'<input type="number" value="{value}" name="{mattr.name}"/>' if value else f'<input type="number" name="{mattr.name}"/>',
            from_db=lambda x: float(x) if x else 0.0,
            from_http=lambda x: float(x) if x else None,
            to_js='*value*',
        ),
        
        MetaAttrType("obj", "object", lambda mattr, value, obj: select_choice(mattr.name, QObject.list_names('all'), value),
            from_http=lambda x: QObject.find_by_name(x),
            to_js='"*value*"',
        ),

        MetaAttrType("rgn", "region", lambda mattr, value, obj: select_choice(mattr.name, QObject.list_names('regn'), value),
            from_http=lambda x: QObject.find_by_name(x),
            to_js='"*value*"',
        ),

        MetaAttrType("itm", "item", lambda mattr, value, obj: select_choice(mattr.name, QObject.list_names('item'), value),
            from_http=lambda x: QObject.find_by_name(x),
            to_js='"*value*"',
        ),

        MetaAttrType("loc", "location", lambda mattr, value, obj: select_choice(mattr.name, QObject.list_names('room'), value),
            from_http=lambda x: QObject.find_by_name(x),
            to_js='"*value*"',
        ),

        MetaAttrType("nob", "object, not editable", lambda mattr, value, obj: value.name,
            from_http=lambda x: QObject.find_by_name(x),
            to_js='"*value*"',
        ),
        



        MetaAttrType("chc", "choice", lambda mattr, value, obj: select_choice(mattr.name, mattr.options(), value),
            from_http=lambda x: x,
            to_js='"*value*"',
        ),

        MetaAttrType("gdr", "gender", lambda mattr, value, obj: select_choice(mattr.name, GENDER_OPTIONS, value),
            from_http=lambda x: x,
            to_js='lang.pronouns.*value*',
        ),

        MetaAttrType("dir", "direction", lambda mattr, value, obj: select_choice(mattr.name, DIRECTIONS, value),
            from_http=lambda x: x,
            to_js='"*value*"',
        ),

        MetaAttrType("cbx", "boolean flag", lambda mattr, value, obj: f'<input type="checkbox" name="{mattr.name}" checked/>' if value else  f'<input type="checkbox" name="{mattr.name}"/>',
            from_db=lambda x: x == 'True',
            from_http=lambda x: x == 'True',
            to_js=lambda x: 'true' if x else 'false',
            default=False,
        ),
        
        # a button sets or unsets an attribute, and then saves; use for templates as they change the buttons on the top
        MetaAttrType("btn", "button", lambda mattr, value, obj: f'Set<input type="hidden" name={mattr.name} value="yes" />' if value else '<input type="button" value="Add" onclick="template_button(\'' + mattr.name + '\')"/>',
            from_http=lambda x: x == 'True',
            to_js=lambda x: 'true' if x else 'false',
        ),  

        MetaAttrType("spc", "special", lambda mattr, value, obj: obj.get_special_widget(mattr.name),
            to_js=lambda x: '',
        ),
                
        MetaAttrType("imp", "implemetation notes", '<textarea rows="7" cols="120" name="*name*">*value*</textarea>',
            big_widget=True,
            from_http=lambda x: '' if not x else x,
            help_text='Use to note what you still have to do or what you did it this way. This will not be part of your published game.',
        ),
        
        MetaAttrType("nul", "Not a proper attribute", '',
        ),
            
                
        # exits are complicated as they contain lots of attributes themselves
        # do we do them as objects?
        # or as complex attributes?
        # attributes:
        #    loc
        #    destination (or nowhere)
        #    direction
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
        MetaAttrType("ext", "exit", lambda mattr, value, obj: obj.get_special_widget(mattr.name),
        ),
    )


    name = models.CharField(max_length=20)
    display_name = models.CharField(max_length=20)
    page = models.ForeignKey(MetaPage, on_delete=models.CASCADE)    
    order = models.IntegerField(default=-1)
    advanced = models.BooleanField(default=False)
    attr_type = models.CharField(max_length=3)
    help_text = models.TextField()
    category = models.CharField(max_length=4, default='item')  # item, room, sttg, game, opts, exit, regn
    rules = models.TextField()
    options_as_string = models.TextField(default='')
    return_type= models.CharField(max_length=12, blank=True, null=True)
    params = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return 'MetaAttr("' + self.name + '")'
        
    def get_type(self):
        try:
            return next(x for x in MetaAttr.TYPE_CHOICES if x.code == self.attr_type)
        except StopIteration as exc:
            raise RuntimeError('Failed to find self.attr_type=' + self.attr_type) from exc


    

    # Convert the given value to the appropriate type. Eg if the attr_type is a cbx, it will
    # be converted to a Boolean. Uses lambdas in the array to do this.
    def to_type(self, value):
        # Unit tested
        t = self.get_type()
        return (t.from_db(value) if t.from_db else value)
        
    def get_help_text(self):
        # Unit tested
        s = self.help_text
        if self.get_type().help_text:
            s += ' ' + self.get_type().help_text
        return s
        
    def options(self):
        return self.options_as_string.split('|')
        
        
    # Find the MetaAttr with the given data
    @staticmethod
    def get(name, category):
        try:
            return MetaAttr.objects.get(name=name, category=category)
        except MetaAttr.DoesNotExist as exc:
            raise RuntimeError(f"Failed to find MetaAttr with name={name} category={category}") from exc




class QGame(models.Model):
    name = models.CharField(max_length=50)
    version = models.IntegerField()

    def __str__(self):
        return 'QGame("' + self.name + '")'


class QObject(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=4, default='item')  # item, room or sttg
    qgame = models.ForeignKey(QGame, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
        
    def title_name(self):
        if self.category == 'exit':
            return 'Exit ' + self.get_attr('direction') + ' from ' + self.get_attr('loc').name + ' to ' + self.get_attr('destination').name
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
        
        
    def create_link(self, dest, dr):
        if self == dest:
            raise ValueError("Trying to create link from a location to itself")
        ext2 = dest.create_exit(self, reverse_dir(dr))
        ext1 = self.create_exit(dest, dr)
        return  ext1, ext2

    def create_exit(self, dest, dr):
        ext = QObject.objects.create(name='__exit_' + self.name + '_' + dr, category='exit', qgame=self.qgame)
        ext.set_attr('loc', self)
        ext.set_attr('destination', dest)
        ext.set_attr('direction', dr)
        ext.set_attr('exit_type', 'Exit')
        return ext
      
      
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
                #print(original_set.first().value)
                #print(attr.to_type(original_set.first().value))
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
        

    # Get an object list of items that have this as the location
    def _get_contents_attrs(self, attr_name, category):
        loc_attr = MetaAttr.objects.get(name=attr_name, category=category)
        return QAttr.objects.filter(attr=loc_attr, value=self.name)


    def get_contents(self, attr_name='loc', category='item'):
        #qattrs = get_contents_attrs()
        lst = []
        for qattr in self._get_contents_attrs(attr_name, category):
            lst.append(qattr.qobject)
        return lst

    def has_contents(self, attr_name='loc'):
        return len(self.get_contents(attr_name)) > 0

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
            
            options = QObject.list_names('room')
            s += '<br/>New exit to: '
            s += select_choice('destination', options, None)
            s += '<br/><input type="checkbox" id="exit-is-link"/>Exit in reverse direction too?'
        
            #s = '<input type="text" id="add-item-' + self.name + '"/> [<span class="clickable" onclick="add_obj(\'item\', \'' + self.name + '\')">Add</span>]'

            #META_ATTRS['room']['exitsRoom']['attrs'].append((dr, f'Go {dr} exit.', True, 'ext',  '', 'An exit in the selected direction.'))
            
            
            return s

        return 'Unrecognised list type: ' + name
            

    # Do this as a property so Django templates can use it
    @property
    def expanded(self):
        return self.get_attr('expanded')



    @staticmethod
    def get_settings():
        return QObject.find_by_name('settings')
    
    
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
            
    @staticmethod
    def list(option):
        if option == 'all':
            return QObject.objects.all().order_by('name')
        else:
            return QObject.objects.filter(category=option).order_by('name')
            

    # Return a list of items that have no location set
    @staticmethod
    def get_by_attr(category, attr_name, value):
        mattr = MetaAttr.objects.get(category=category, name=attr_name)
        lst = []
        for qattr in QAttr.objects.filter(attr=mattr, value=value):
            lst.append(qattr.qobject)
        return lst


    # Return a list of items that do not have the given attribute
    @staticmethod
    def get_not_attr(category, attr_name):
        mattr = MetaAttr.objects.get(category=category, name=attr_name)
        all_objs = QObject.objects.filter(category=category).order_by('name')
        
        exclude = []
        for qattr in QAttr.objects.filter(attr=mattr):
            exclude.append(qattr.qobject)
        return [x for x in all_objs if x not in exclude]



            

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


          
    # Returns a list of duplicated names
    @staticmethod
    def get_duplicates():
        #print('here')
        names = QObject.list_names('all')
        seen = set()
        seen_add = seen.add
        # adds all elements it doesn't know yet to seen and all other to seen_twice
        seen_twice = set( x for x in names if x in seen or seen_add(x) )
        # turn the set into a list (as requested)
        return list(seen_twice)




class QAttr(models.Model):
    value = models.TextField()

    attr = models.ForeignKey(MetaAttr, on_delete=models.CASCADE)
    qobject = models.ForeignKey(QObject, on_delete=models.CASCADE)

    def __str__(self):
        return self.qobject.name + '->' + self.attr.name + ' = ' + self.value
        
    # use the property value to get the value as it is stored in the database, a string
    # use this to get it as the correct type
    def get_value(self):
        return self.attr.to_type(self.value)
        
        

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
    
    qgame = QGame.objects.create(name='example', version=VERSION)

    for cat in META_ATTRS:
        for idx, key in enumerate(META_ATTRS[cat]):
            meta = META_ATTRS[cat][key]
            page = MetaPage.objects.create(name=key, alias=meta['alias'], category=cat, order=idx)
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
            

    o = QObject.objects.create(name='settings', category='sttg')
    for data in INIT_OBJECTS:
        o = QObject.objects.create(name=data[0], category=data[1], qgame=qgame)
            
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
        
    hall = QObject.find_by_name('hall')
    lounge = QObject.find_by_name('lounge')
    kitchen = QObject.find_by_name('kitchen')
    hall.create_link(lounge, 'west')
    hall.create_link(kitchen, 'south')
            