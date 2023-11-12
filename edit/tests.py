from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .utils import *
from .models import *
from edit.templatetags.helpers import *






class UtilsTests(TestCase):

    def test_test_rule(self):
        page = MetaPage.objects.create(name="test")
        MetaAttr.objects.create(name="name", page=page, display_name='', attr_type='id')
        MetaAttr.objects.create(name="big", page=page, display_name='', attr_type='cbx')
        MetaAttr.objects.create(name="small", page=page, display_name='', attr_type='cbx')
        item = QObject.objects.create(category='item')
        item.set_attr('name', 'red ball')
        item.set_attr('big', False)
        item.set_attr('small', True)

        self.assertEqual(test_rule(item, "flag=big"), False)
        self.assertEqual(test_rule(item, "flag=small"), True)
        self.assertEqual(test_rule(item, "!flag=big"), True)
        self.assertEqual(test_rule(item, "!flag=small"), False)


    def test_test_rules1(self):
        page = MetaPage.objects.create(name="test", rules="flag=big")
        MetaAttr.objects.create(name="big", page=page, display_name='', attr_type='cbx')
        item = QObject.objects.create(category='item')
        item.set_attr('big', False)

        self.assertEqual(test_rules(item, page), False)


    def test_test_rules2(self):
        page = MetaPage.objects.create(name="test", rules="flag=big")
        MetaAttr.objects.create(name="big", page=page, display_name='', attr_type='cbx')
        item = QObject.objects.create(category='item')
        item.set_attr('big', True)

        self.assertEqual(test_rules(item, page), True)


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












class MetaPageTests(TestCase):

    def test_get_all(self):
        page1 = MetaPage.objects.create(name="test", category='room')
        page2 = MetaPage.objects.create(name="test", category='room')
        page3 = MetaPage.objects.create(name="test", category='item')
        room = QObject.objects.create(category='room')
        item = QObject.objects.create(category='item')

        self.assertEqual(len(MetaPage.get_all(room)), 2)
        self.assertEqual(len(MetaPage.get_all(item)), 1)


    def test_get_some(self):
        page1 = MetaPage.objects.create(name="test1", category='item')
        page2 = MetaPage.objects.create(name="test2", category='item', rules='flag=big')
        page3 = MetaPage.objects.create(name="test3", category='item', rules='flag=small')
        MetaAttr.objects.create(name="name", page=page1, display_name='', attr_type='id')
        MetaAttr.objects.create(name="big", page=page2, display_name='', attr_type='cbx')
        MetaAttr.objects.create(name="small", page=page3, display_name='', attr_type='cbx')
        item = QObject.objects.create(category='item')
        item.set_attr('name', 'red ball')
        item.set_attr('big', False)
        item.set_attr('small', True)

        lst = MetaPage.get_some(item)
        self.assertEqual(len(lst), 2)
        self.assertEqual(lst[0], page1)
        self.assertEqual(lst[1], page3)
        




class MetaAttrTests(TestCase):

    def test_to_type(self):
        page = MetaPage.objects.create(name="test")
        mattr1 = MetaAttr.objects.create(name="name", page=page, display_name='', attr_type='id')
        mattr2 = MetaAttr.objects.create(name="alias", page=page, display_name='', attr_type='str')
        mattr3 = MetaAttr.objects.create(name="size", page=page, display_name='', attr_type='int')
        mattr4 = MetaAttr.objects.create(name="big", page=page, display_name='', attr_type='cbx')

        self.assertEqual(mattr1.get_type()[0], 'id')
        self.assertEqual(mattr2.get_type()[0], 'str')
        self.assertEqual(mattr2.to_type('house'), 'house')
        self.assertEqual(mattr3.to_type('5'), 5)
        self.assertEqual(mattr4.to_type('True'), True)


    def test_attr_row(self):
        page = MetaPage.objects.create(name="test")
        mattr = MetaAttr.objects.create(name="obj1", page=page, display_name='', attr_type='str', category='item')
        room = QObject.objects.create(category='room')
        item = QObject.objects.create(category='item')
        attr = QAttr.objects.create(value="pretty", qobject=item, attr=mattr)
        s = attr_row(mattr, item)
        self.assertEqual(s, '<tr title=""><td><b></b></td><td><input type="text" value="pretty" name="obj1"/></td><td> </td></tr>')
        s = attr_row(mattr, room)
        self.assertEqual(s, '')


    def test_attr_row_select(self):
        self.maxDiff = None
        page = MetaPage.objects.create(name="test")
        mattr = MetaAttr.objects.create(name="loc", page=page, display_name='', attr_type='loc', category='item')
        QObject.objects.create(name='lounge', category='room')
        QObject.objects.create(name='hall', category='room')
        item = QObject.objects.create(category='item')
        #attr = QAttr.objects.create(value="pretty", qobject=item, attr=mattr)
        s = attr_row(mattr, item)
        self.assertEqual(s, '<tr title=""><td><b></b></td><td>  <select id="loc" name="loc" style="width:300px;" data-valid="yes">\n    <option value="-1" selected>--- Select ---</option>\n    <option value="hall">hall</option>\n    <option value="lounge">lounge</option>\n  </select>\n</td><td> </td></tr>')
        
        
    def test_help_text(self):
        page = MetaPage.objects.create(name="test")
        mattr = MetaAttr.objects.create(name="name", page=page, display_name='', help_text='part.', attr_type='id')
        self.assertEqual(mattr.get_help_text(), 'part. Can only contain standard letters and numbers, plus underscore.')





class QObjectTests(TestCase):

    def test_attr(self):
        page = MetaPage.objects.create(name="test")
        MetaAttr.objects.create(name="name", page=page, display_name='', attr_type='id')
        MetaAttr.objects.create(name="alias", page=page, display_name='', attr_type='str')
        MetaAttr.objects.create(name="size", page=page, display_name='', attr_type='int')
        MetaAttr.objects.create(name="big", page=page, display_name='', attr_type='cbx')
        MetaAttr.objects.create(name="small", page=page, display_name='', attr_type='cbx')
        item = QObject.objects.create(category='item')
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
        page = MetaPage.objects.create(name="test")
        MetaAttr.objects.create(name="name", page=page, display_name='', attr_type='id')
        MetaAttr.objects.create(name="alias", page=page, display_name='', attr_type='str')
        MetaAttr.objects.create(name="size", page=page, display_name='', attr_type='int')
        MetaAttr.objects.create(name="big", page=page, display_name='', attr_type='cbx')
        MetaAttr.objects.create(name="small", page=page, display_name='', attr_type='cbx')
        item = QObject.objects.create(category='item')
        item.set_attr('name', 'red ball')
        item.set_attr('alias', 'the red ball')
        item.set_attr('size', 7)
        item.set_attr('big', False)
        item.set_attr('small', True)

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
        





class JSTests(TestCase):
    def test_to_js(self):
        page = MetaPage.objects.create(name="test")
        MetaAttr.objects.create(name="alias", page=page, display_name='', attr_type='str')
        MetaAttr.objects.create(name="big", page=page, display_name='', attr_type='cbx')
        MetaAttr.objects.create(name="small", page=page, display_name='', attr_type='cbx')
        MetaAttr.objects.create(name="list", page=page, display_name='', attr_type='say')
        item = QObject.objects.create(category='item')
        
        attr = item.set_attr('alias', 'the red ball')
        self.assertEqual(attr.to_js(), '  alias:"the red ball",\n')
        attr = item.set_attr('big', False)
        self.assertEqual(attr.to_js(), '  big:false,\n')
        attr = item.set_attr('small', True)
        self.assertEqual(attr.to_js(), '  small:true,\n')
        attr = item.set_attr('list', 'one|two|three')
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
        page = MetaPage.objects.create(name="test")
        MetaPage.objects.create(name="templates")
        MetaAttr.objects.create(name="name", page=page, display_name='', attr_type='id')
        MetaAttr.objects.create(name="alias", page=page, display_name='', attr_type='str')
        MetaAttr.objects.create(name="size", page=page, display_name='', attr_type='int')
        item = QObject.objects.create(name='ball', category='item')
        
        item.set_attr('alias', 'the red ball')
        item.set_attr('size', 7)
        self.assertEqual(item.to_js(), 'createItem("ball", {\n  alias:"the red ball",\n  size:7,\n})\n\n')
        
            
    def test_to_js_object_choice(self):
        page = MetaPage.objects.create(name="test")
        MetaPage.objects.create(name="templates")
        MetaAttr.objects.create(name="name", page=page, display_name='', attr_type='id')
        MetaAttr.objects.create(name="alias", page=page, display_name='', attr_type='str')
        MetaAttr.objects.create(name="gender", page=page, display_name='', attr_type='gdr')
        item = QObject.objects.create(name='Lara', category='item')
        
        item.set_attr('alias', 'Lara Rabbit')
        item.set_attr('gender', 'female')
        self.assertEqual(item.to_js(), 'createItem("Lara", {\n  alias:"Lara Rabbit",\n  gender:pronouns.female,\n})\n\n')
        
            
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





        
        
class QObjectStaticTests(TestCase):
        
    def test_find(self):
        page = MetaPage.objects.create(name="test")
        MetaAttr.objects.create(name="name", page=page, display_name='', attr_type='id')
        item = QObject.objects.create(category='item')
        item.set_attr('name', 'red ball')
        item2 = QObject.objects.create(category='item')
        item2.set_attr('name', 'blue ball')
        item3 = QObject.objects.create(category='item')
        item3.set_attr('name', 'green ball')
        
        o = QObject.find_by_name('red ball')
        self.assertEqual(o, item)
        o = QObject.find_by_name('nonsense')
        self.assertEqual(o, None)


    def test_list(self):
        page = MetaPage.objects.create(name="test")
        MetaAttr.objects.create(name="name", page=page, display_name='', attr_type='id')
        item = QObject.objects.create(name='ball', category='item')
        item = QObject.objects.create(name='hat', category='item')
        item = QObject.objects.create(name='lounge', category='room')
        item = QObject.objects.create(name='hall', category='room')
        lst = QObject.list_names('all')
        self.assertEqual(len(lst), 4)
        self.assertEqual(lst[0], 'ball')
        lst = QObject.list_names('room')
        self.assertEqual(len(lst), 2)
        self.assertEqual(lst[0], 'hall')
        
        
        
        
        
        
class KickStartTests(TestCase):
        
        
    def test_kick_start(self):
        kick_start()
        self.assertEqual(len(QObject.objects.all()), 7)







class ViewTests(TestCase):
    def test_list(self):
        response = self.client.get(reverse("edit:object_list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["room_list"], [])        
        self.assertQuerySetEqual(response.context["item_list"], [])        