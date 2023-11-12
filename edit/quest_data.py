

GENDER_OPTIONS = [
    ("thirdperson", "Third person (it, its)"),
    ("firstperson", "First person (I, my)"),
    ("secondperson", "Second person (you, yours)"),
    ("male", "Male (he, his)"),
    ("female", "Female (she, her)"),
    ("nonbinary", "Non-binary (they, their; singular)"),
    ("plural", "Plural (they, their)"),
    ("massnoun", "Mass noun (it, its)"),
]

DIRECTIONS = [
  'north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest',
  'in', 'out', 'up', 'down',
]




META_ATTRS = {
    'homeSttg':{
        'alias':'Home',
        'category':'sttg',
        'home':True,
        'attrs':[
            #('name',           'Name',          False, 'str',  '', 'Not used (to be hidden or somethong!).'),
            ('title',           'Title',         False, 'str',  '', 'The name of your game.'),
            ('subtitle',        'Sub-Title',     False, 'str',  '', 'An optional sub-title.'),
            ('playMode',        'Play mode',     False, 'str',  '', 'Should be dev, beta or play.'),
            ('author',          'Author',        False, 'str',  '', 'Your name (or pen name).'),
            ('version',         'Version',       False, 'str',  '', 'Stored as a string; remember to update when you start a new version.'),
        ],
    },
    
    
    'homeRoom':{
        'alias':'Home',
        'category':'room',
        'home':True,
        'attrs':[
            ('name',           'Name',            False, 'id',  '', 'This is the name that the game uses internally.'),
        ],
    },
    
    
    'homeItem':{
        'alias':'Home',
        'category':'item',
        'home':True,
        'attrs':[
            ('name',           'Name',            False, 'id',  '', 'This is the name that the game uses internally.'),
            ('gender',         'Gender',          False, 'gdr', '', 'Determines the pronouns to use.'),
            ('loc',            'Location',        False, 'obj', '', 'The name of the object where this item is located.'),
            ('scenery',        'Scenery',         False, 'cbx', '', 'Is this item scenery?'),
            ('parserPriority', 'Parsr priority',  True,  'int', '', 'Give a bonus, making this item more like;y to be chosen by the parser (or negative to be less likely).'),
            ('excludeFromAll', 'Exclude from all',True,  'cbx', '', 'Do not include this item when user does GET ALL, etc.'),
        ],
    },
    
    

    
    

    'namingRoom':{
        'alias':'Naming',
        'category':'room',
        'attrs':[
            ('alias',          'Alias',           False, 'str', '', 'This is the name that appears to the user; unlike the "name" attribute, any character is allowed.'),
            ('headingAlias',   'Heading alias',   True,  'str', '', 'How the location should appear in the heading (defaults to the alias)'),
            ('properNoun',     'Proper noun',     True,  'cbx', '', 'Should the name get capitalised?'),
        ],
    },
    
    'namingItem':{
        'alias':'Naming',
        'category':'item',
        'attrs':[
            ('alias',          'Alias',           False, 'str', '', 'This is the name that appears to the user; unlike the "name" attribute, any character is allowed.'),
            ('synonyms',       'Synonyms',        False, 'say', '', 'All the other words the user might use to refer to this object.'),
            ('properNoun',     'Proper noun',     True,  'cbx', '', 'Should the name get capitalised?'),
            ('regex',          'Regex',           True,  'rgx', '', 'User input can be matched against this'),
            ('pluralAlias',    'Plural alias',    True,  'str', '', 'How it should be written as a plural (not generally needed)'),
            ('listAlias',      'List alias',      True,  'str', '', 'How the item should appear in the side pane (defaults to the alias)'),
            ('owner',          'Owner',           False, 'obj', '', 'An item can have an owner; it will then get referred to as such.'),
        ],
    },
    
    
    
    'descriptionsRoom':{
        'alias':'Descriptions',
        'category':'room',
        'attrs':[
            ('desc',           'Description',     False, 'txt', '', 'This text will be displayed when the player enters the location or types LOOK.'),
            ('darkDesc',       'Desc. when dark', True,  'txt', '', 'This text will be displayed when the player enters the location or types LOOK and it is dark.'),
            ('smell',          'Smell',           True,  'txt', '', 'What can the player smell here?'),
            ('listen',         'Listen',          True,  'txt', '', 'What can the player hear?'),
        ],
    },

    'descriptionsItem':{
        'alias':'Descriptions',
        'category':'item',
        'attrs':[
            ('examine',        'Description',     False, 'txt', '', 'This text will be displayed when the player examines the object.'),
        ],
    },





    'scripts':{
        'alias':'Scripts',
        'category':'room',
        'attrs':[
            ('beforeFirstEnter', 'Before first enter', True, 'scr',  '', 'A script that will run when the player enters the room for the first time, before the room description is displayed.', None, None),
            ('beforeEnter', 'Before enter',            True, 'scr',  '', 'A script that will run each time the player enters the room, before the room description is displayed.', None, None),
            ('afterFirstEnter', 'After first enter',   True, 'scr',  '', 'A script that will run when the player enters the room for the first time, after the room description is displayed.', None, None),
            ('afterEnter', 'After enter',              True, 'scr',  '', 'A script that will run each time the player enters the room, after the room description is displayed.', None, None),
            ('isLocatedAt', 'Location script',         True, 'scr',  '', 'A script that should return true if the item is here; passed the name of the location.', None, None),
        ],
    },
    



    'templates':{
        'alias':'Templates',
        'category':'item',
        'help_link':'templates',
        'attrs':[
            ('takeable',       'Takeable',        False, 'btn', '', 'This item can be picked up (and is not wearable).'),
            ('wearable',       'Wearable',        False, 'btn', '', 'This item is a garment or similar that can be worn.'),
            ('npc',            'NPC',             False, 'btn', '', 'This item is an NPC - another character in the game world.'),
            ('player',         'The player',      False, 'btn', '', 'This item is the player. You need one, and only one, of these in your game.'),
        ],
    },


    'takeable':{
        'alias':'Takeable',
        'category':'item',
        'help_link':'takeable',
        'rules':'flag=takeable',
        'attrs':[
            ('testTake',    'Can this be taken?',    True, 'scr', '', 'Script run before this item is picked up; return true if allowed.', 'boolean', 'options'),
            ('testDrop',  'Can this be dropped?', True, 'scr', '', 'Script run before this item is dropped; return true if allowed.', 'boolean', 'options'),
            ('afterMove',   'After moving script', True, 'scr', '', 'Script run after this item is moved to a different location.', None, 'obj obj'),
        ],
    },


    'wearable':{
        'alias':'Wearable',
        'category':'item',
        'help_link':'wearable',
        'rules':'flag=wearable',
        'attrs':[
            ('layer',       'Layer',                False, 'int', '', 'Suggest 1 for underwear, 2 for shirt and pnts, 3 for coats'),
            ('slots',       'Slots',                False, 'say', '', 'List the body parts covered.'),
            ('worn',        'Worn at start?',       False, 'cbx', '', 'Tick this to have the item start the game worn by someone. You must also give it a suitable location - whoever is wearing it.'),
            ('armour',      'Armour rating',        True, 'int', '', 'Optionally assign an armour value, if applicable to your game.'),
            ('testWear',    'Can this be worn?',    True, 'scr', '', 'Script run before this garment is put on; return true if allowed.', 'boolean', 'options'),
            ('testRemove',  'Can this be removed?', True, 'scr', '', 'Script run before this garment is removed; return true if allowed.', 'boolean', 'options'),
            ('afterWear',   'After wearing script', True, 'scr', '', 'Script run after this garment is put on.', None, 'options'),
            ('afterRemove', 'After removal script', True, 'scr', '', 'Script run after this garment is removed.', None, 'options'),
        ],
    },


    'npc':{
        'alias':'NPC',
        'category':'item',
        'help_link':'npc',
        'rules':'flag=npc',
        'attrs':[
            ('agenda',       'Agenda',              False, 'say', '', 'A list of actions this NPC will do'),
            ('reactions',    'Reactions',           False, 'say', '', 'A list of reactions'),
            ('askOptions',   'Ask options',         False, 'say', '', 'A list of responses to ASK/ABOUT.'),
            ('tellOptions',  'Ask options',         False, 'say', '', 'A list of responses to TELL/ABOUT.'),
        ],
    },

    'player':{
        'alias':'Player',
        'category':'item',
        'help_link':'player',
        'rules':'flag=player',
        'attrs':[
        ],
    },




    'exitsRoom':{
        'alias':'Exits',
        'category':'room',
        'attrs':[
            # add these later
        ],
    },

    'exitsItem':{
        'alias':'Exits',
        'category':'item',
        'attrs':[
            ('goInDirection', 'Go in direction',      True, 'dir',  '', 'Going IN to this item takes the player through the exit in the selected direction.'),
            ('goOutDirection', 'Go out direction',    True, 'dir',  '', 'Going OUT of this item takes the player through the exit in the selected direction.'),
            ('goUpDirection', 'Go up direction',      True, 'dir',  '', 'Going UP this item takes the player through the exit in the selected direction.'),
            ('goDownDirection', 'Go down direction',  True, 'dir',  '', 'Going DOWN this item takes the player through the exit in the selected direction.'),
            ('goThroughDirection', 'Go through dir.', True, 'dir',  '', 'Going THROUGH this item takes the player through the exit in the selected direction.'),
        ],
    },
}

for dr in DIRECTIONS:
    META_ATTRS['exitsRoom']['attrs'].append((dr, f'Go {dr} exit.', True, 'ext',  '', 'An exit in the selected direction.'))


INIT_OBJECTS = [
    ('player', False),
    ('lounge', True),
    ('kitchen', True),
    ('hat', False),
    ('ball', False),
    ('Lara', False),
]


INIT_ATTRS = [
    ('settings', 'title', 'My QuestJS Game'),
    ('settings', 'author', 'The Pixie'),
    ('settings', 'version', '0.1'),
    ('player', 'alias', 'player'),
    ('player', 'synonyms', 'me|myself'),
    ('player', 'loc', 'lounge'),
    ('player', 'player', True),
    ('player', 'examine', 'Looking good!'),
    ('lounge', 'desc', 'A bit of a mess!'),
    ('kitchen', 'desc', 'Sparking clean!'),
    ('hat', 'wearable', True),
    ('hat', 'loc', 'kitchen'),
    ('ball', 'takeable', True),
    ('Lara', 'npc', True),
    ('Lara', 'gender', 'female'),
    ('Lara', 'loc', 'lounge'),
    ('Lara', 'examine', 'A normal-sized rabbit with a carrot obsession.'),
]
