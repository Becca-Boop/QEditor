from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .utils import *
from .models import *
from edit.templatetags.helpers import *




def setup():
    page1 = MetaPage.objects.create(name="test1", category='room')
    page2 = MetaPage.objects.create(name="test2", category='room')
    page3 = MetaPage.objects.create(name="test3", category='item')

    MetaAttr.objects.create(name="name", page=page1, display_name='', attr_type='id', category='room')
    MetaAttr.objects.create(name="alias", page=page1, display_name='', attr_type='str', category='room')

    MetaAttr.objects.create(name="name", page=page3, display_name='', attr_type='id')
    MetaAttr.objects.create(name="alias", page=page3, display_name='', attr_type='str')
    MetaAttr.objects.create(name="size", page=page3, display_name='', attr_type='int')
    MetaAttr.objects.create(name="big", page=page3, display_name='', attr_type='cbx')
    MetaAttr.objects.create(name="small", page=page3, display_name='', attr_type='cbx')
    MetaAttr.objects.create(name="option", page=page3, display_name='', attr_type='chc', options_as_string='one|two|three')

    qgame = QGame.objects.create(name='example', version=0, subversion=1)

    item = QObject.objects.create(category='item', qgame=qgame)
    room = QObject.objects.create(category='room', qgame=qgame)
    return item, room




class UtilsTests(TestCase):

    def test_test_rule_boolean(self):
        item, room = setup()
        
        item.set_attr('name', 'red ball')
        item.set_attr('big', False)
        item.set_attr('small', True)

        self.assertEqual(test_rule(item, None, "big=True"), False)
        self.assertEqual(test_rule(item, None, "small=True"), True)
        self.assertEqual(test_rule(item, None, "big=False"), True)
        self.assertEqual(test_rule(item, None, "small=False"), False)


    def test_test_rule_str(self):
        item, room = setup()
        item = QObject.objects.create(category='item')
        item.set_attr('name', 'red ball')
        item.set_attr('alias', 'test string')
        item.set_attr('option', 'three')

        self.assertEqual(test_rule(item, None, "alias=test string"), True)
        self.assertEqual(test_rule(item, None, "!alias=test string"), False)
        self.assertEqual(test_rule(item, None, "alias=wrong string"), False)
        self.assertEqual(test_rule(item, None, "!alias=wrong string"), True)

        self.assertEqual(test_rule(item, None, "option=three"), True)
        self.assertEqual(test_rule(item, None, "option=two"), False)


    def test_test_rules1(self):
        page = MetaPage.objects.create(name="test", rules="big=True")
        MetaAttr.objects.create(name="big", page=page, display_name='', attr_type='cbx')
        item = QObject.objects.create(category='item')
        item.set_attr('big', False)

        self.assertEqual(test_rules(item, None, page), False)


    def test_test_rules2(self):
        # The @ says we should use the second object for the rule, not the first
        page = MetaPage.objects.create(name="test", rules="@big=True")
        MetaAttr.objects.create(name="big", page=page, display_name='', attr_type='cbx')
        item = QObject.objects.create(category='item')
        item2 = QObject.objects.create(category='item')
        item.set_attr('big', True)

        # The second item is not big, so rule returns false
        self.assertEqual(test_rules(item, item2, page), False)
        item2.set_attr('big', True)
        # The second item is now big, so rule returns true
        self.assertEqual(test_rules(item, item2, page), True)


    def test_test_rules2(self):
        page = MetaPage.objects.create(name="test", rules="big=True")
        MetaAttr.objects.create(name="big", page=page, display_name='', attr_type='cbx')
        item = QObject.objects.create(category='item')
        item.set_attr('big', True)

        self.assertEqual(test_rules(item, None, page), True)


    def test_select_choice_with_strings(self):
        self.maxDiff = None
        
        list = ['Lara', 'ball5', 'hat', 'kitchen']
        
        s = select_choice('loc', list, None)
        expected = '  <select id="loc" name="loc" style="width:300px;" data-valid="yes">\n    <option value="-1" selected>--- Select ---</option>\n    <option value="Lara">Lara</option>\n    <option value="ball5">ball5</option>\n    <option value="hat">hat</option>\n    <option value="kitchen">kitchen</option>\n  </select>\n'
        self.assertEqual(s, expected)

        s = select_choice('loc', list, 'kitchen')
        expected = '  <select id="loc" name="loc" style="width:300px;" data-valid="yes">\n    <option value="-1">-- Select --</option>\n    <option value="Lara">Lara</option>\n    <option value="ball5">ball5</option>\n    <option value="hat">hat</option>\n    <option value="kitchen" selected>kitchen</option>\n  </select>\n'
        self.assertEqual(s, expected)


    def test_select_choice_with_tuples(self):
        self.maxDiff = None
        
        list = [('l', 'Lara'), ('b', 'ball5'), ('h', 'hat'), ('k', 'kitchen')]
        
        s = select_choice('loc', list, None)
        expected = '  <select id="loc" name="loc" style="width:300px;" data-valid="yes">\n    <option value="-1" selected>--- Select ---</option>\n    <option value="l">Lara</option>\n    <option value="b">ball5</option>\n    <option value="h">hat</option>\n    <option value="k">kitchen</option>\n  </select>\n'
        self.assertEqual(s, expected)

        s = select_choice('loc', list, 'k')
        expected = '  <select id="loc" name="loc" style="width:300px;" data-valid="yes">\n    <option value="-1">-- Select --</option>\n    <option value="l">Lara</option>\n    <option value="b">ball5</option>\n    <option value="h">hat</option>\n    <option value="k" selected>kitchen</option>\n  </select>\n'
        self.assertEqual(s, expected)


    def test_get_special_widget(self):
        page = MetaPage.objects.create(name="test", category='item')
        MetaAttr.objects.create(name="loc", page=page, display_name='', attr_type='obj')
        MetaAttr.objects.create(name="alias", page=page, display_name='', attr_type='str') # needed even if not used!
        room = QObject.objects.create(category='room', name='lounge')
        item1 = QObject.objects.create(category='item', name='one')
        item2 = QObject.objects.create(category='item', name='two')
        item3 = QObject.objects.create(category='item', name='three')
        item1.set_attr('loc', 'lounge')
        item2.set_attr('loc', 'lounge')

        s = room.get_special_widget('item-list')
        expected = '<ul><li><a href="/edit/object/2" target="_blank">one</a></li><li><a href="/edit/object/3" target="_blank">two</a></li></ul>'
        expected += '<input type="text" id="add-item-lounge" class="restricted-input"/> [<span class="clickable" onclick="add_obj(\'item\', \'lounge\')">Add</span>]'

        self.assertEqual(s, expected)




class MetaPageTests(TestCase):

    def test_get_all(self):
        item, room = setup()

        self.assertEqual(len(MetaPage.get_all(room)), 2)
        self.assertEqual(len(MetaPage.get_all(item)), 1)


    def test_get_some(self):
        page1 = MetaPage.objects.create(name="test1", category='item')
        page2 = MetaPage.objects.create(name="test2", category='item', rules='big=True')
        page3 = MetaPage.objects.create(name="test3", category='item', rules='small=True')
        MetaAttr.objects.create(name="name", page=page1, display_name='', attr_type='id')
        MetaAttr.objects.create(name="big", page=page2, display_name='', attr_type='cbx')
        MetaAttr.objects.create(name="small", page=page3, display_name='', attr_type='cbx')
        qgame = QGame.objects.create(name='example', version=0, subversion=1)
        item = QObject.objects.create(category='item', qgame=qgame)
        item.set_attr('name', 'red ball')
        item.set_attr('big', False)
        item.set_attr('small', True)

        lst = MetaPage.get_some(item)
        self.assertEqual(len(lst), 2)
        self.assertEqual(lst[0], page1)
        self.assertEqual(lst[1], page3)
        



class MetaAttrTests(TestCase):




    def test_attr_row(self):
        item, room = setup()
        page = MetaPage.objects.create(name="test")
        mattr = MetaAttr.objects.create(name="obj1", page=page, display_name='', attr_type='str', category='item')
        attr = QAttr.objects.create(value="pretty", qobject=item, attr=mattr)
        
        s = attr_row(mattr, item)
        s_ex = '<tr title=""><td><b></b></td><td><input type="text" value="pretty" name="obj1"/></td><td></td></tr>'
        self.assertEqual(s, s_ex)
        s = attr_row(mattr, room)
        self.assertEqual(s, '')


    def test_attr_row_select(self):
        self.maxDiff = None
        page = MetaPage.objects.create(name="test")
        mattr = MetaAttr.objects.create(name="loc", page=page, display_name='', attr_type='loc', category='item')
        qgame = QGame.objects.create(name='example', version=0, subversion=1)
        QObject.objects.create(name='lounge', category='room', qgame=qgame)
        QObject.objects.create(name='hall', category='room', qgame=qgame)
        item = QObject.objects.create(category='item', qgame=qgame)
        #attr = QAttr.objects.create(value="pretty", qobject=item, attr=mattr)
        s = attr_row(mattr, item)
        s_ex = '<tr title=""><td><b></b></td><td>  <select id="loc" name="loc" style="width:300px;" data-valid="yes">\n    <option value="-1" selected>--- Select ---</option>\n    <option value="hall">hall</option>\n    <option value="lounge">lounge</option>\n  </select>\n</td><td></td></tr>'
        self.assertEqual(s, s_ex)
        
        
    def test_help_text(self):
        page = MetaPage.objects.create(name="test")
        mattr = MetaAttr.objects.create(name="name", page=page, display_name='', help_text='part.', attr_type='id')
        self.assertEqual(mattr.get_help_text(), 'part. Can only contain standard letters and numbers, plus underscore.')





class QAttrTests(TestCase):
    def test_get_attr(self):
        item, room = setup()
        page = MetaPage.objects.create(name="test")
        mattr1 = MetaAttr.objects.create(name="alias", page=page, display_name='', attr_type='str')
        mattr2 = MetaAttr.objects.create(name="size", page=page, display_name='', attr_type='int')
        mattr3 = MetaAttr.objects.create(name="flag", page=page, display_name='', attr_type='cbx')
        attr1 = QAttr.objects.create(attr=mattr1, qobject=item, value='Hello World')
        attr2 = QAttr.objects.create(attr=mattr2, qobject=item, value=42)
        attr3 = QAttr.objects.create(attr=mattr3, qobject=item, value='True')
        
        self.assertEqual(attr1.get_value(), 'Hello World')
        self.assertEqual(attr2.get_value(), 42)
        self.assertEqual(attr3.get_value(), True)







  
        
class QGameTests(TestCase):


    def test_get_version(self):
        qgame = QGame.objects.create(name='example', version=3, subversion=2)
        self.assertEqual(qgame.get_version(), '3.2')
        

        
    def test_find(self):
        page = MetaPage.objects.create(name="test")
        MetaAttr.objects.create(name="name", page=page, display_name='', attr_type='id')
        qgame = QGame.objects.create(name='example', version=0, subversion=1)
        item = QObject.objects.create(category='item', qgame=qgame)
        item.set_attr('name', 'red ball')
        item2 = QObject.objects.create(category='item', qgame=qgame)
        item2.set_attr('name', 'blue ball')
        item3 = QObject.objects.create(category='item', qgame=qgame)
        item3.set_attr('name', 'green ball')
        
        o = qgame.find_by_name('red ball')
        self.assertEqual(o, item)
        o = qgame.find_by_name('nonsense')
        self.assertEqual(o, None)


    def test_list(self):
        page = MetaPage.objects.create(name="test")
        MetaAttr.objects.create(name="name", page=page, display_name='', attr_type='id')
        qgame = QGame.objects.create(name='example', version=0, subversion=1)
        item = QObject.objects.create(name='ball', category='item', qgame=qgame)
        item = QObject.objects.create(name='hat', category='item', qgame=qgame)
        item = QObject.objects.create(name='lounge', category='room', qgame=qgame)
        item = QObject.objects.create(name='hall', category='room', qgame=qgame)
        lst = qgame.list_names('all')
        self.assertEqual(len(lst), 4)
        self.assertEqual(lst[0], 'ball')
        lst = qgame.list_names('room')
        self.assertEqual(len(lst), 2)
        self.assertEqual(lst[0], 'hall')
        
        






class QObjectTests(TestCase):

    def test_set_attr(self):
        item, room = setup()
        
        count1 = QAttr.objects.all().count()
        item.set_attr('name', 'red ball')
        item.set_attr('alias', 'the red ball')
        item.set_attr('size', 7)
        item.set_attr('big', False)
        item.set_attr('small', True)
        count2 = QAttr.objects.all().count()
        self.assertEqual(count2, count1 + 4)



    def test_attr_defaults(self):
        item, room = setup()

        item.set_attr('name', 'red ball')

        self.assertEqual(item.get_attr('alias'), '')
        self.assertEqual(item.get_attr('size'), 0)
        self.assertEqual(item.get_attr('big'), False)
        self.assertEqual(item.get_attr('small'), False)
        
        
        
    
    def test_get_attr(self):
        item, room = setup()

        item.set_attr('name', 'red ball')
        item.set_attr('alias', 'the red ball')
        item.set_attr('size', 7)
        item.set_attr('big', False)
        item.set_attr('small', True)
        item2 = QObject.objects.create(category='item')
        item2.set_attr('name', 'blue ball')
        item3 = QObject.objects.create(category='item')
        item3.set_attr('name', 'green ball')
        
        self.assertEqual(item.__str__(), 'red ball')
        self.assertEqual(item.get_attr('name'), 'red ball')
        self.assertEqual(item.get_attr('alias'), 'the red ball')
        self.assertEqual(item.get_attr('size'), 7)
        self.assertEqual(item.get_attr('big'), False)
        self.assertEqual(item.get_attr('small'), True)



    def test_update(self):
        item, room = setup()
        item.set_attr('name', 'red ball')
        item.set_attr('alias', 'the red ball')
        item.set_attr('size', 7)
        item.set_attr('big', False)
        item.set_attr('small', True)
        page = MetaPage.objects.get(name='test3')

        item.update({
            'name':'blue ball',
            'alias':'the blue ball',
            'size':10,
            'big':True,
        }, page)

        self.assertEqual(item.get_attr('name'), 'blue ball')
        self.assertEqual(item.get_attr('alias'), 'the blue ball')
        self.assertEqual(item.get_attr('size'), 10)
        self.assertEqual(item.get_attr('big'), True)
        self.assertEqual(item.get_attr('small'), False)
        


    def test_contents(self):
        page = MetaPage.objects.create(name="test", category='item')
        MetaAttr.objects.create(name="loc", page=page, display_name='', attr_type='loc', category='item')
        MetaAttr.objects.create(name="alias", page=page, display_name='', attr_type='str') # needed even if not used!
        qgame = QGame.objects.create(name='example', version=0, subversion=1)
        room = QObject.objects.create(category='room', name='lounge')
        item1 = QObject.objects.create(category='item', name='one')
        item2 = QObject.objects.create(category='item', name='two')
        item3 = QObject.objects.create(category='item', name='three')
        
        self.assertEqual(room.get_contents(), [])
        self.assertEqual(room.has_contents(), False)
        
        item1.set_attr('loc', 'lounge')
        item2.set_attr('loc', 'lounge')

        self.assertEqual(room.get_contents(), [item1, item2])
        self.assertEqual(room.has_contents(), True)


    def test_get_by_attr(self):
        page = MetaPage.objects.create(name="test", category='item')
        MetaAttr.objects.create(name="loc", page=page, display_name='', attr_type='loc', category='item')
        MetaAttr.objects.create(name="alias", page=page, display_name='', attr_type='str')
        qgame = QGame.objects.create(name='example', version=0, subversion=1)
        room = QObject.objects.create(category='room', name='lounge', qgame=qgame)
        item1 = QObject.objects.create(category='item', name='one', qgame=qgame)
        item2 = QObject.objects.create(category='item', name='two', qgame=qgame)
        item3 = QObject.objects.create(category='item', name='three', qgame=qgame)
        

        item1.set_attr('alias', 'one')
        self.assertEqual(qgame.get_by_attr('item', 'alias', 'one'), [item1])
        self.assertEqual(qgame.get_not_attr('item', 'alias'), [item3, item2])
        self.assertEqual(qgame.get_by_attr('item', 'loc', 'lounge'), [])
        
        item1.set_attr('loc', 'lounge')
        item2.set_attr('loc', 'lounge')

        self.assertEqual(qgame.get_by_attr('item', 'loc', 'lounge'), [item1, item2])
        self.assertEqual(qgame.get_not_attr('item', 'loc'), [item3])




class QObjectExitTests(TestCase):

    def test_exits(self):
        page = MetaPage.objects.create(name="test")
        MetaAttr.objects.create(name="loc", page=page, category='exit', display_name='Location', attr_type='loc')
        MetaAttr.objects.create(name="exit_type", page=page, category='exit', display_name='Exit type', attr_type='chc')
        MetaAttr.objects.create(name="destination", page=page, category='exit', display_name='Destination', attr_type='loc')
        MetaAttr.objects.create(name="direction", page=page, category='exit', display_name='Location', attr_type='str')
        qgame = QGame.objects.create(name='example', version=0, subversion=1)

        lounge = QObject.objects.create(category='room', name='lounge', qgame=qgame)
        hall = QObject.objects.create(category='room', name='hall', qgame=qgame)
        ext1, ext2 = lounge.create_link(hall, 'north')
        
        self.assertEqual(ext1.name, '__exit_lounge_north')
        
        ext = hall.find_exit('south')
        self.assertEqual(ext, ext2)
        self.assertEqual(ext.get_attr('direction'), 'south')
        self.assertEqual(ext.get_attr_as_s('loc'), 'hall')
        self.assertEqual(ext.get_attr('loc'), hall)
        self.assertEqual(ext.get_attr_as_s('destination'), 'lounge')
        self.assertEqual(ext.get_attr('destination'), lounge)
        ext = hall.find_exit('north')
        self.assertEqual(ext, None)
        


class JSObjectTests(TestCase):
    def test_to_js(self):
        item, room = setup()
        page = MetaPage.objects.get(name='test3')
        MetaAttr.objects.create(name="list", page=page, display_name='', attr_type='say')
        
        attr = item.set_attr('alias', 'the red ball')
        self.assertEqual(attr.to_js(), '  alias:"the red ball",\n')
        attr = item.set_attr('big', False)
        self.assertEqual(attr.to_js(), '  big:false,\n')
        attr = item.set_attr('small', True)
        self.assertEqual(attr.to_js(), '  small:true,\n')
        attr = item.set_attr('list', 'one\ntwo\nthree')
        self.assertEqual(attr.to_js(), '  list:[\n    "one",\n    "two",\n    "three",\n  ],\n')

        
    def test_to_js_int(self):
        page = MetaPage.objects.create(name="test")
        MetaAttr.objects.create(name="width", page=page, display_name='', attr_type='int')
        MetaAttr.objects.create(name="height", page=page, display_name='', attr_type='int')
        MetaAttr.objects.create(name="depth", page=page, display_name='', attr_type='int')
        item = QObject.objects.create(category='item')
        
        attr1 = item.set_attr('width', 7)
        attr2 = item.set_attr('height', 0)
        self.assertEqual(attr1.to_js(), '  width:7,\n')
        self.assertEqual(attr2.to_js(), '  height:0,\n')
        #self.assertEqual(attr.to_js(), '')
        
        
    def test_to_js_template(self):
        page = MetaPage.objects.create(name="templates")
        MetaAttr.objects.create(name="takeable", page=page, display_name='', attr_type='btn')
        item = QObject.objects.create(category='item')
        
        attr = item.set_attr('takeable', True)
        self.assertEqual(attr.to_js(), '  takeable:true,\n')
        
   
    def test_to_js_for_settings(self):
        page = MetaPage.objects.create(name="test")
        MetaAttr.objects.create(name="mode", page=page, display_name='', category='sttg', attr_type='str')
        settings = QObject.objects.create(category='sttg')
        attr = settings.set_attr('mode', 'dev')
        self.assertEqual(attr.to_js(), 'settings.mode = "dev"\n')
        

    def test_to_js_object(self):
        item, room = setup()
        page2 = MetaPage.objects.create(name="templates")
        item.set_attr('name', 'ball')
        item.set_attr('alias', 'the red ball')
        item.set_attr('size', 7)
        s = item.to_js()
        s_exp = 'createItem("ball", {\n  alias:"the red ball",\n  size:7,\n})\n\n'
        self.assertEqual(s, s_exp)
        
            
    def test_to_js_room_and_exit(self):
        item, room = setup()
        page2 = MetaPage.objects.create(name="templates")

        page3 = MetaPage.objects.create(name="test3", category='exit')

        MetaAttr.objects.create(name="name", page=page3, display_name='', attr_type='id')
        MetaAttr.objects.create(name="exit_type", page=page3, display_name='', attr_type='str', category='exit')
        MetaAttr.objects.create(name="direction", page=page3, display_name='', attr_type='str', category='exit')
        MetaAttr.objects.create(name="loc", page=page3, display_name='', attr_type='loc', category='exit')
        MetaAttr.objects.create(name="destination", page=page3, display_name='', attr_type='loc', category='exit')



        room.set_attr('name', 'lounge')
        room.set_attr('alias', 'the modern-looking lounge')
        room.create_exit('lounge', 'north')
        e = room.create_exit(room, 'south')
        e.set_attr('exit_type', 'Exit')
        
        s = room.to_js()
        s_exp = 'createRoom("lounge", {\n  alias:"the modern-looking lounge",\n  north:new Exit("lounge"),\n  south:new Exit("lounge", {\n  }),\n})\n\n'
        
        self.assertEqual(s, s_exp)
        
            
    def test_to_js_object_choice(self):
        page = MetaPage.objects.create(name="test")
        MetaPage.objects.create(name="templates")
        MetaAttr.objects.create(name="name", page=page, display_name='', attr_type='id')
        MetaAttr.objects.create(name="alias", page=page, display_name='', attr_type='str')
        MetaAttr.objects.create(name="gender", page=page, display_name='', attr_type='gdr')
        item = QObject.objects.create(name='Lara', category='item')
        
        item.set_attr('alias', 'Lara Rabbit')
        item.set_attr('gender', 'female')
        self.assertEqual(item.to_js(), 'createItem("Lara", {\n  alias:"Lara Rabbit",\n  gender:lang.pronouns.female,\n})\n\n')
        
            
    def test_to_js_object_template(self):
        page1 = MetaPage.objects.create(name="test")
        page2 = MetaPage.objects.create(name="templates")
        MetaAttr.objects.create(name="name", page=page1, display_name='', attr_type='id')
        MetaAttr.objects.create(name="alias", page=page1, display_name='', attr_type='str')
        MetaAttr.objects.create(name="takeable", page=page2, display_name='', attr_type='btn')
        item = QObject.objects.create(name='ball', category='item')
        
        item.set_attr('alias', 'the red ball')
        item.set_attr('takeable', True)
        self.assertEqual(item.to_js(), 'createItem("ball", TAKEABLE(), {\n  alias:"the red ball",\n  takeable:true,\n})\n\n')



class JSGameTests(TestCase):
    def test_to_js(self):
        item, room = setup()
        page = MetaPage.objects.create(name="templates")
        page = MetaPage.objects.create(name="test")
        MetaAttr.objects.create(name="loc", page=page, category='exit', display_name='Location', attr_type='loc')
        MetaAttr.objects.create(name="exit_type", page=page, category='exit', display_name='Exit type', attr_type='chc')
        MetaAttr.objects.create(name="destination", page=page, category='exit', display_name='Destination', attr_type='loc')
        MetaAttr.objects.create(name="direction", page=page, category='exit', display_name='Location', attr_type='str')

        qgame = QGame.objects.first()
        s = qgame.to_data_js()
        s_exp = '"use strict"\n\ncreateItem("", {\n})\n\ncreateRoom("", {\n})\n\n'
        self.assertEqual(s, s_exp)


      
        
        
        
        
class KickStartTests(TestCase):
        
        
    def test_kick_start(self):
        kick_start()
        self.assertTrue(len(QObject.objects.all()) > 10)




class HelperTests(TestCase):

    def test_hier_obj(self):
        page1 = MetaPage.objects.create(name="test", category='item')
        page2 = MetaPage.objects.create(name="test", category='room')
        MetaAttr.objects.create(name="loc", page=page1, display_name='', attr_type='obj')
        MetaAttr.objects.create(name="alias", page=page1, category='item', display_name='', attr_type='str') # needed even if not used!
        MetaAttr.objects.create(name="alias", page=page2, category='room', display_name='', attr_type='str')
        room = QObject.objects.create(category='room', name='lounge')
        item1 = QObject.objects.create(category='item', name='one')
        item2 = QObject.objects.create(category='item', name='two')
        item3 = QObject.objects.create(category='item', name='three')
        item1.set_attr('loc', 'lounge')
        item2.set_attr('loc', 'lounge')

        s = hier_obj(item1)
        s = hier_obj(room)




class ViewTests(TestCase):
    def test_list(self):
        page = MetaPage.objects.create(name="test", category='item')
        MetaAttr.objects.create(name="loc", page=page, display_name='', attr_type='loc', category='item')
        MetaAttr.objects.create(name="alias", page=page, display_name='', attr_type='str')
        qgame = QGame.objects.create(name='example', version=0, subversion=1)

        response = self.client.get(reverse("edit:object_list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["region_list"], [])        
        self.assertQuerySetEqual(response.context["nowhere_list"], [])        
        


