
"""
Constructs a drop-down menu in HTML with the given data.
Notethat selected is the element, not the index
"""
def select_choice(name, options, selected):
    if hasattr(selected, 'name'):
        selected = selected.name
    #print('-----------')
    #print(name)
    #print(options)
    #print(selected)
    #print(type(selected))
    s =  '  <select id="' + name + '" name="' + name + '" style="width:300px;" data-valid="yes">\n'
    if selected:
        s += '    <option value="-1">-- Select --</option>\n'
    else:
        s += '    <option value="-1" selected>--- Select ---</option>\n'
    for opt in options:
        #print(opt)
        if isinstance(opt, str):
            #print('string')
            s += '    <option value="' + str(opt) + '"'
            if opt == selected:
                #print('match')
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
But the new string in JavaScript code for an array.
"""
def string_array_to_js(list_as_string):
    strg = '[\n'
    for s in list_as_string.split('|'):
        strg += '    "' + s + '",\n'
    strg += '  ]'
    return strg



"""
Returns true if this object should have the given page displayed,
based on category and rules
"""
def test_rules(obj, mpage):
    if obj.category != mpage.category:
        return False
    if not mpage.rules:
        return True
    rules = mpage.rules.split()
    for rule in rules:
        if not test_rule(obj, rule):
            #print(rule)
            return False
    return True


"""
Returns true if this object conforms to the given rule.
Should only be used by test_rules
"""
def test_rule(obj, rule):
    left, right = rule.split('=')
    value = obj.get_attr(right)
    if left == 'flag':
        return value
    if left == '!flag':
        return not value
    return True



