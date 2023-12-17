
"""
Constructs a drop-down menu in HTML with the given data.
Note that selected is the element (the HTML value, which is actually the name for a dictionary), not the index
"""
def select_choice(name, options, selected):
    if hasattr(selected, 'name'):
        selected = selected.name
    s =  '  <select id="' + name + '" name="' + name + '" style="width:300px;" data-valid="yes">\n'
    if selected:
        s += '    <option value="-1">-- Select --</option>\n'
    else:
        s += '    <option value="-1" selected>--- Select ---</option>\n'
    for opt in options:
        if isinstance(opt, str):
            s += '    <option value="' + str(opt) + '"'
            if opt == selected:
                s += ' selected'
            s += '>' + opt + '</option>\n'
        else:
            s += '    <option value="' + str(opt[0]) + '"'
            if opt[0] == selected:
                s += ' selected'
            s += '>' + opt[1] + '</option>\n'
    s += '  </select>\n'
    return s
   


"""
Converts a string into another string!
But the new string is JavaScript code for an array.
"""
def string_array_to_js(list_as_string, sep):
    strg = '[\n'
    for s in list_as_string.split(sep):
        strg += '    "' + s + '",\n'
    strg += '  ]'
    return strg



"""
Returns true if this object should have the given page displayed,
based on category and rules
"""
def test_rules(obj, settings, mpage):
    if obj.category != mpage.category:
        return False
    if not mpage.rules:
        return True
    rules = mpage.rules.split()
    for rule in rules:
        if not test_rule(obj, settings, rule):
            return False
    return True


"""
Returns true if this object conforms to the given rule.
Should only be used by test_rules
Examples:

flag=npc    # true if the object has npc set to true
!flag=npc    # true if the object has npc set to false
male=gender  # true if the object has gender set to male, false otherwise

"""
def test_rule(obj, settings, rule):
    left, right = rule.split('=')
    inverted = False
    if left.startswith('!'):
        inverted = True
        left = left[1:]
    if left.startswith('@'):
        obj = settings
        left = left[1:]
    value = obj.get_attr(left)
    result = right == str(value)
    if inverted:
        return not result
    return result







####  EXITS  #####


# Give an HTML snippet for a table cell for the exit of the object in the given direction
def exit_td(obj, dr):
    ext = obj.find_exit(dr)
    if ext:
        s = '<td>'
        s += '<a href="/edit/object/' + str(ext.id) + '" target="_blank"><b>' + dr + '</b></a>'
        s += ' (' + ext.get_attr('destination').name + ')'
        return s + '</td>'
    
    else:
        return '<td onclick="create_exit(\'' + dr + '\')" class="clickable">' + dr + '</td>'

REVERSE = {
    'north':'south',
    'northeast':'southwest',
    'east':'west',
    'southeast':'northwest',
    'south':'north',
    'southwest':'northeast',
    'west':'east',
    'northwest':'sotheast',
    'in':'out',
    'out':'in',
    'up':'down',
    'down':'up',
}
        
def reverse_dir(dr):
    return REVERSE[dr]