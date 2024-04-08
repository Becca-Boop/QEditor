

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


# NOTES
# Cannot use rules with cbx or btn because of the way HTTP transfers booleans - the absence of a name-value pairs is assumed to indicate False

META_ATTRS = {
    'sttg':{
        'homeSttg':{
            'alias':'Home',
            'category':'sttg',
            'home':True,
            'attrs':[
                ('title',           'Title',         False, 'str',  '', 'The name of your game.'),
                ('subtitle',        'Sub-Title',     False, 'str',  '', 'An optional sub-title.'),
                ('playMode',        'Play mode',     False, 'str',  '', 'Should be dev, beta or play.'),
                ('author',          'Author',        False, 'str',  '', 'Your name (or pen name).'),
                ('version',         'Version',       False, 'str',  '', 'Stored as a string; remember to update when you start a new version.'),
                ('conversations',   'Conversation style', False, 'chc', '', 'How will the player chat to NPCs?', {'none':'None', 'simple':'Simple TALK TO', 'dynamic':'Dynamic TALK TO', 'askabout':'ASK/ABOUT'}),  # !!! TODO writing as JS
            ],
        },
    },
    
    'regn':{
        'homeRegion':{
            'alias':'Home',
            'category':'regn',
            'home':True,
            'attrs':[
                ('name',           'Name',            False, 'id',  '', 'This is the name that the game uses internally.'),
                ('expanded',       'Start expanded',  False, 'cbx', '', 'Should this region be opened up when you load the home page?'),
                ('notes',          'Notes',           False, 'imp',  '', "Notes about what you still need to do can go here."),
            ],
        },    
    },    
    
    'room':{
        'homeRoom':{
            'alias':'Home',
            'home':True,
            'attrs':[
                ('name',           'Name',          False, 'id',  '', 'This is the name that the game uses internally.'),
                ('region',         'Region',        False, 'rgn', '', 'Assign locations to regions to keep them organised.'),
                ('item-list',      'Items here',    False, 'spc',  '', "These items are at this location (go to the item's own page to change its location)"),
                ('notes',          'Notes',         False, 'imp',  '', "Notes about what you still need to do can go here."),
            ],
        },
        
        'namingRoom':{
            'alias':'Naming',
            'attrs':[
                ('alias',          'Alias',           False, 'str', '', 'This is the name that appears to the user; unlike the "name" attribute, any character is allowed.'),
                ('headingAlias',   'Heading alias',   True,  'str', '', 'How the location should appear in the heading (defaults to the alias)'),
                ('properNoun',     'Proper noun',     True,  'cbx', '', 'Should the name get capitalised?'),
            ],
        },
        
        'descriptionsRoom':{
            'alias':'Descriptions',
            'attrs':[
                ('desc',           'Description',     False, 'txt', '', 'This text will be displayed when the player enters the location or types LOOK.'),
                ('darkDesc',       'Desc. when dark', True,  'txt', '', 'This text will be displayed when the player enters the location or types LOOK and it is dark.'),
                ('smell',          'Smell',           True,  'txt', '', 'What can the player smell here?'),
                ('listen',         'Listen',          True,  'txt', '', 'What can the player hear?'),
            ],
        },

        'scripts':{
            'alias':'Scripts',
            'attrs':[
                ('beforeFirstEnter', 'Before first enter', True, 'scr',  '', 'A script that will run when the player enters the room for the first time, before the room description is displayed.', None, None),
                ('beforeEnter', 'Before enter',            True, 'scr',  '', 'A script that will run each time the player enters the room, before the room description is displayed.', None, None),
                ('afterFirstEnter', 'After first enter',   True, 'scr',  '', 'A script that will run when the player enters the room for the first time, after the room description is displayed.', None, None),
                ('afterEnter', 'After enter',              True, 'scr',  '', 'A script that will run each time the player enters the room, after the room description is displayed.', None, None),
                ('isLocatedAt', 'Location script',         True, 'scr',  '', 'A script that should return true if the item is here; passed the name of the location.', None, None),
            ],
        },

        'exitsRoom':{
            'alias':'Exits',
            'attrs':[
                ('exits',           'Exits',            False, 'ext',  '', 'Exits from this location to another.'),
            ],
        },
    },

    'item':{
        'homeItem':{
            'alias':'Home',
            'home':True,
            'attrs':[
                ('name',           'Name',            False, 'id',  '', 'This is the name that the game uses internally.'),
                ('gender',         'Gender',          False, 'gdr', '', 'Determines the pronouns to use.'),
                ('loc',            'Location',        False, 'obj', '', 'The name of the object where this item is located.'),
                ('scenery',        'Scenery',         False, 'cbx', '', 'Is this item scenery?'),
                ('parserPriority', 'Parser priority',  True,  'int', '', 'Give a bonus, making this item more likely to be chosen by the parser (or negative to be less likely).'),
                ('excludeFromAll', 'Exclude from all',True,  'cbx', '', 'Do not include this item when user does GET ALL, etc.'),
                ('item-list',      'Items here',      False, 'spc',  '', "These items are contained by this item"),
            ],
        },

        'namingItem':{
            'alias':'Naming',
            'attrs':[
                ('alias',          'Alias',           False, 'str', '', 'This is the name that appears to the user; unlike the "name" attribute, any character is allowed.'),
                ('synonyms',       'Synonyms',        False, 'say', '', 'All the other words the user might use to refer to this object.'),
                ('properNoun',     'Proper noun',     True,  'cbx', '', 'Should the name get capitalised?'),
                ('regex',          'Regex',           True,  'rgx', '', 'User input can be matched against this'),
                ('pluralAlias',    'Plural alias',    True,  'str', '', 'How it should be written as a plural (not generally needed)'),
                ('listAlias',      'List alias',      True,  'str', '', 'How the item should appear in the side pane (defaults to the alias)'),
                ('owner',          'Owner',           False, 'obj', '', 'An item can -optionally - have an owner; it will then get referred to as such.'),
            ],
        },

        'descriptionsItem':{
            'alias':'Descriptions',
            'attrs':[
                ('examine',        'Description',     False, 'txt', '', 'This text will be displayed when the player examines the object.'),
                ('smell',          'Smell',           True,  'txt', '', 'What can the player smell from the item?'),
                ('listen',         'Listen',          True,  'txt', '', 'What can the player hear from the item?'),
            ],
        },

        'templates':{
            'alias':'Templates',
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
            'help_link':'takeable',
            'rules':'takeable=True',
            'attrs':[
                ('testTake',    'Can this be taken?',    True, 'scr', '', 'Script run before this item is picked up; return true if allowed.', 'boolean', 'options'),
                ('testDrop',  'Can this be dropped?', True, 'scr', '', 'Script run before this item is dropped; return true if allowed.', 'boolean', 'options'),
                ('afterMove',   'After moving script', True, 'scr', '', 'Script run after this item is moved to a different location.', None, 'obj obj'),
            ],
        },


        'wearable':{
            'alias':'Wearable',
            'help_link':'wearable',
            'rules':'wearable=True',
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
            'help_link':'npc',
            'rules':'npc=True',
            'attrs':[
                ('agenda',       'Agenda',              False, 'say', '', 'A list of actions this NPC will do'),
                ('reactions',    'Reactions',           False, 'say', '', 'A list of reactions'),
                ('none',         'Conversations',       False, 'nul', '!@conversations=ASK/ABOUT !@conversations=S', 'Select a conversation mode from settings and the appropriate options will appear here.'),
                ('askOptions',   'Ask options',         False, 'say', '@conversations=ASK/ABOUT', 'A list of responses to ASK/ABOUT.'),
                ('tellOptions',  'Ask options',         False, 'say', '@conversations=ASK/ABOUT', 'A list of responses to TELL/ABOUT.'),
            ],
        },


        #        ('conversations',   'Conversation style', False, 'chc', '', 'How will the player chat to NPCs?', ['None', 'Simple TALK TO', 'Dynamic TALK TO', 'ASK/ABOUT']),




        'player':{
            'alias':'Player',
            'help_link':'player',
            'rules':'player=True',
            'attrs':[
            ],
        },

        'exitsItem':{
            'alias':'Exits',
            'rules':'!npc=True !player=True',
            'attrs':[
                ('goInDirection', 'Go in direction',      True, 'dir',  '', 'Going IN to this item takes the player through the exit in the selected direction.'),
                ('goOutDirection', 'Go out direction',    True, 'dir',  '', 'Going OUT of this item takes the player through the exit in the selected direction.'),
                ('goUpDirection', 'Go up direction',      True, 'dir',  '', 'Going UP this item takes the player through the exit in the selected direction.'),
                ('goDownDirection', 'Go down direction',  True, 'dir',  '', 'Going DOWN this item takes the player through the exit in the selected direction.'),
                ('goThroughDirection', 'Go through dir.', True, 'dir',  '', 'Going THROUGH this item takes the player through the exit in the selected direction.'),
            ],
        },
    },

    'exit':{
        'homeExit':{
            'alias':'Home',
            'help_link':'exit',
            'category':'regn',
            'home':True,
            'attrs':[
                ('loc',            'Origin',            False, 'nob',  '', 'The exit starts from here.'),
                ('direction',      'Direction',         False, 'nst',  '', 'North, south, in, out, etc.'),
                ('destination',    'Destination',       False, 'loc',  '', 'The exit will take the player to this location.'),
                ('exit_type',      'Exit type',         True,  'chc',  '', "Special exits can be set up using an alternative type.", ['Simple', 'Exit', 'NonExit', 'BarredExit', 'WayIn', 'WayOut', 'ClimbExit', 'StairsUp', 'StrairsDown']),
                ('related_item',  'Related item',       True,  'itm',  '', "Only for WayIn, ClimbExit, StairsUp and StairsDown."),
                ('msg',            'Message when used', False, 'txt',  '', "Used when the player uses the exit."),
                ('scenery',        'Scenery',           False,  'cbx',  '', "Is this exit scenery?"),
                ('hidden',         'Hidden',            False,  'cbx',  '', "Is this exit hidden?"),
                ('lit',            'Lit',               False,  'cbx',  '', "Is this exit self-illuminated?"),
                ('locked',         'Locked',            False,  'cbx',  '', "Is this exit locked?"),
                ('lockedMsg',      'Locked message',    False,  'txt',  '', "If locked, the player will see this."),
                ('alsoDir',        'Also directions',   True,   'say',  '', "User can aso use these directions to use this exit."),

                ('simpleUse',      'Script',            True,  'scr',  '', "Script to run when used.", 'Boolean', 'options'),
                ('npcLeaveMsg',    'When used by NPC',  True,  'txt',  '', "Used when the NPCr uses the exit to leave the room the player is in."),
                ('npcEnterMsg',    'When used by NPC',  True,  'txt',  '', "Used when the NPCr uses the exit to enter the room the player is in."),
                ('msgNpc',         'When used by NPC',  True,  'scr',  '', "Script used when the NPCr uses the exit.", None, 'options'),
            ],
        },    
    }
}

#for dr in DIRECTIONS:
#    META_ATTRS['room']['exitsRoom']['attrs'].append((dr, f'Go {dr} exit.', True, 'ext',  '', 'An exit in the selected direction.'))


INIT_OBJECTS = [
    ('player', 'item'),
    ('lounge', 'room'),
    ('kitchen', 'room'),
    ('hall', 'room'),
    ('street', 'room'),
    ('inside', 'regn'),
    ('outside', 'regn'),
    ('hat', 'item'),
    ('ball', 'item'),
    ('Lara', 'item'),
]


INIT_EXITS = [
    ('Simple', 'kitchen', 'hall', 'north'),
    ('Simple', 'hall', 'kitchen', 'south'),
    ('Exit', 'lounge', 'hall', 'west'),
    ('Exit', 'hall', 'lounge', 'east', 'You head east, though the great door.'),

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

    ('inside', 'expanded', True),
    
    ('lounge', 'desc', 'A bit of a mess!'),
    ('lounge', 'region', 'inside'),

    ('kitchen', 'desc', 'Sparking clean!'),
    ('kitchen', 'region', 'inside'),

    ('hall', 'desc', 'Rather elegant.'),
    ('hall', 'region', 'inside'),

    ('street', 'desc', 'a long, winding street...'),
    ('street', 'region', 'outside'),

    ('hat', 'wearable', True),
    ('hat', 'loc', 'kitchen'),

    ('ball', 'takeable', True),

    ('Lara', 'npc', True),
    ('Lara', 'gender', 'female'),
    ('Lara', 'loc', 'lounge'),
    ('Lara', 'examine', 'A normal-sized rabbit with a carrot obsession.'),  
]
