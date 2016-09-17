#!/usr/bin/python

#----------------------------------------------------------------------

debug = False

class Condition:
    def print_type(self):
        print "<Condition Type, 2 lines"

    def print_data(self):
        print "<Condition Data>"

class Condition_Always(Condition):
    def print_type(self):
        print "i"
        print "1"

    def print_data(self):
        print "i"
        print "0"

class Condition_Chat(Condition):
    def __init__(self, text):
        self.text = text

    def print_type(self):
        print "i"
        print "4"

    def print_data(self):
        print "s"
        print self.text

class Condition_InventoryItemCountLE(Condition):
    def __init__(self, item, count):
        self.item = item
        self.count = int(count)

    def print_type(self):
        print "i"
        print "11"

    def print_data(self):
        print "TABLE"
        print "2"
        print "k"
        print "v"
        print "n"
        print "n"
        print "2"
        # n (name) = name
        print "s"
        print "n"
        print "s"
        print self.item
        # c (count) = count
        print "s"
        print "c"
        print "i"
        print self.count

class Condition_All(Condition):
    def __init__(self, conditions):
        self.conditions = conditions

    def print_type(self):
        print "i"
        print "2"

    def print_data(self):
        print "TABLE"
        print "2"
        print "K"
        print "V"
        print "n"
        print "n"
        print len(self.conditions)
        for condition in self.conditions:
            condition.print_type()
            condition.print_data()

class Condition_Not(Condition):
    def __init__(self, condition):
        self.condition = condition

    def print_type(self):
        print "i"
        print "21"

    def print_data(self):
        print "TABLE"
        print "2"
        print "K"
        print "V"
        print "n"
        print "n"
        print "1"
        self.condition.print_type()
        self.condition.print_data()

class Condition_SecondsInStateGE(Condition):
    def __init__(self, seconds):
        self.seconds = int(seconds)

    def print_type(self):
        print "i"
        print "6"

    def print_data(self):
        print "i"
        print self.seconds

#----------------------------------------------------------------------

class Action:
    def print_type(self):
        print "<Action Type, 2 lines..."

    def print_data(self):
        print "<Action Data>"

class CallState(Action):
    def __init__(self, state, return_state):
        self.state = state
        self.return_state = return_state

    def print_type(self):
        print "i"
        print "5"

    def print_data(self):
        print "TABLE"
        print "2"
        print "k"
        print "v"
        print "n"
        print "n"
        print "2"
        # st = self.state
        print "s"
        print "st"
        print "s"
        print self.state
        # ret = self.return_state
        print "s"
        print "ret"
        print "s"
        print self.return_state

class ChatCommand(Action):
    def __init__(self, text):
        self.text = text

    def print_type(self):
        print "i"
        print "2"

    def print_data(self):
        print "s"
        print self.text

class ChatExpression(Action):
    def __init__(self, text):
        self.text = text

    def print_type(self):
        print "i"
        print "8"

    def print_data(self):
        print "TABLE"
        print "2"
        print "k"
        print "v"
        print "n"
        print "n"
        print "1"

        print "s"
        print "e"
        print "s"
        print self.text

class AllCommand(Action):
    def __init__(self, commands):
        self.commands = commands

    def print_type(self):
        print "i"
        print "3"

    def print_data(self):
        print "TABLE"
        print "2"
        print "K"
        print "V"
        print "n"
        print "n"
        print len(self.commands)
        for command in self.commands:
            command.print_type()
            command.print_data()

class SetMetaState(Action):
    def __init__(self, state):
        self.state = state

    def print_type(self):
        print "i"
        print "1"

    def print_data(self):
        print "s"
        print self.state

class ExprAction(Action):
    def __init__(self, text):
        self.text = text

    def print_type(self):
        print "i"
        print "7"

    def print_data(self):
        print "TABLE"
        print "2"
        print "k"
        print "v"
        print "n"
        print "n"
        print "1"
        print "s"
        print "e"
        print "s"
        print self.text

class ReturnFromCall(Action):
    def print_type(self):
        print "i"
        print "6"

    def print_data(self):
        print "i"
        print "0"

#----------------------------------------------------------------------

class Rule:
    def __init__(self, state, condition, action):
        self.state = state
        self.condition = condition
        self.action = action

    def generate_meta(self):
        if debug:
            print "# Rule:"
        self.condition.print_type()
        self.action.print_type()
        self.condition.print_data()
        self.action.print_data()
        print "s"
        print self.state

#----------------------------------------------------------------------


if 0:
    Rule("Default",             Condition_Chat("!item"),                                                         CallState("MakeItem", "Default"))

    Rule("InfuseIntrospection", Condition_InventoryItemCountLE("Quill of Introspection", 0),                     ChatCommand("/s Need Quill of Introspection"))
    Rule("InfuseIntrospection", Condition_InventoryItemCountLE("Quill of Introspection", 0),                     SetMetaState("Default"))
    Rule("InfuseIntrospection", Condition_InventoryItemCountLE("Mana Scarab", 0),                                ChatCommand("/s Need Mana Scarab"))
    Rule("InfuseIntrospection", Condition_InventoryItemCountLE("Mana Scarab", 0),                                SetMetaState("Default"))
    Rule("InfuseIntrospection", Condition_Always(),                                                              ExprAction("actiontryapplyitem[ wobjectfindininventorybyname[Quill of Introspection], wobjectfindininventorybyname[Mana Scarab]]"))
    Rule("InfuseIntrospection", Condition_Always(),                                                              ReturnFromCall())

    Rule("MakeIntroObject",     Condition_InventoryItemCountLE("Infused Quill of Introspection", 0),             CallState("InfuseIntrospection", "MakeIntroObject"))
    Rule("MakeIntroObject",     Condition_InventoryItemCountLE("Ink of Objectification", 0),                     ChatCommand("/s Need Ink of Objectification"))
    Rule("MakeIntroObject",     Condition_InventoryItemCountLE("Ink of Objectification", 0),                     SetMetaState("Default"))
    Rule("MakeIntroObject",     Condition_Always(),                                                              ExprAction("actiontryapplyitem[ wobjectfindininventorybyname[Infused Quill of Introspection], wobjectfindininventorybyname[Ink of Objectification]]"))
    Rule("MakeIntroObject",     Condition_Always(),                                                              ReturnFromCall())

    Rule("MakeBDSelf",          Condition_InventoryItemCountLE("Introspective Quill of Objectification", 0),     CallState("MakeIntroObject", "MakeBDSelf"))
    Rule("MakeBDSelf",          Condition_InventoryItemCountLE("Glyph of Strength", 0),                          ChatCommand("/s Need Glyph of Strength"))
    Rule("MakeBDSelf",          Condition_InventoryItemCountLE("Glyph of Strength", 0),                          SetMetaState("Default"))
    Rule("MakeBDSelf",          Condition_Always(),                                                              ExprAction("actiontryapplyitem[ wobjectfindininventorybyname[Introspective Quill of Objectification], wobjectfindininventorybyname[Glyph of Strength]]"))
    Rule("MakeBDSelf",          Condition_Always(),                                                              ReturnFromCall())

    Rule("MakeItem",            Condition_InventoryItemCountLE("Inscription of Aura of Blood Drinker Self", 0),  CallState("MakeBDSelf", "MakeItem"))
    Rule("MakeItem",            Condition_Always(),                                                              ChatCommands("/s Done making level 8 Item scrolls."))
    Rule("MakeItem",            Condition_Always(),                                                              SetMetaState("Default"))


#----------------------------------------------------------------------

if 0:
    # Basic components don't get made, just need them on hand.
    Rule("Make Mana Scarab",                               Condition_Always(),                                                              AllCommand([ChatCommand("/s Need Mana Scarab"),
                                                                                                                                                        SetMetaState("Default")
                                                                                                                                                        ]))

    Rule("Make Quill of Introspection",                    Condition_Always(),                                                              AllCommand([ChatCommand("/s Need Quill of Introspection"),
                                                                                                                                                        SetMetaState("Default")
                                                                                                                                                        ]))

    Rule("Make Ink of Objectification",                    Condition_Always(),                                                              AllCommand([ChatCommand("/s Need Ink of Objectification"),
                                                                                                                                                        SetMetaState("Default")
                                                                                                                                                        ]))

    Rule("Make Glyph of Strength",                         Condition_Always(),                                                              AllCommand([ChatCommand("/s Need Glyph of Strength"),
                                                                                                                                                        SetMetaState("Default")
                                                                                                                                                        ]))

    Rule("Make Glyph of Melee Defense",                    Condition_Always(),                                                              AllCommand([ChatCommand("/s Need Glyph of Melee Defense"),
                                                                                                                                                        SetMetaState("Default")
                                                                                                                                                        ]))

    Rule("Make Infused Quill of Introspection",            Condition_All([Condition_InventoryItemCountLE("Infused Quill of Introspection", 0),
                                                                          Condition_InventoryItemCountLE("Quill of Introspection", 0)
                                                                          ]),                                                                           CallState("Make Quill of Introspection", "Make Infused Quill of Introspection"))
    Rule("Make Infused Quill of Introspection",            Condition_All([Condition_InventoryItemCountLE("Infused Quill of Intorspection", 0),
                                                                          Condition_InventoryItemCountLE("Mana Scarab", 0)
                                                                          ]),                                                                           CallState("Make Mana Scarab",            "Make Infused Quill of Introspection"))
    Rule("Make Infused Quill of Introspection",            Condition_All([Condition_Not(Condition_InventoryItemCountLE("Quill of Introspection", 0)),
                                                                          Condition_Not(Condition_InventoryItemCountLE("Mana Scarab", 0)),
                                                                          ConditionInventoryItemCountLE("Infused Quill of Introspection", 0)
                                                                          ]),                                                                          AllCommand([ExprAction("actiontryapplyitem[ wobjectfindininventorybyname[Quill of Introspection], wobjectfindininventorybyname[Mana Scarab]]"),
                                                                                                                                                                   ReturnFromCall()
                                                                                                                                                                   ]))

    #Rule("Make Introspective Quill of Objectification",    Condition_InventoryItemCountLE("Infused Quill of Introspection", 0),             CallState("Make Infused Quill of Introspection", "Make Introspective Quill of Objectification"))
    #Rule("Make Introspective Quill of Objectification",    Condition_InventoryItemCountLE("Ink of Objectification", 0),                     CallState("Make Ink of Objectification",         "Make Introspective Quill of Objectification"))
    #Rule("Make Introspective Quill of Objectification",    Condition_Always(),                                                              ExprAction("actiontryapplyitem[ wobjectfindininventorybyname[Infused Quill of Introspection], wobjectfindininventorybyname[Ink of Objectification]]"))
    #Rule("Make Introspective Quill of Objectification",    Condition_Always(),                                                              ReturnFromCall())

    #Rule("Make Inscription of Aura of Blood Drinker Self", Condition_InventoryItemCountLE("Introspective Quill of Objectification", 0),     CallState("Make Introspective Quill of Objectification", "Make Inscription of Aura of Blood Drinker Self"))
    #Rule("Make Inscription of Aura of Blood Drinker Self", Condition_InventoryItemCountLE("Glyph of Strength", 0),                          CallState("Make Glyph of Strength",                      "Make Inscription of Aura of Blood Drinker Self"))
    #Rule("Make Inscription of Aura of Blood Drinker Self", Condition_Always(),                                                              ExprAction("actiontryapplyitem[ wobjectfindininventorybyname[Introspective Quill of Objectification], wobjectfindininventorybyname[Glyph of Strength]]"))
    #Rule("Make Inscription of Aura of Blood Drinker Self", Condition_Always(),                                                              ReturnFromCall())

    #Rule("Make Inscription of Aura of Defender Self",      Condition_InventoryItemCountLE("Introspective Quill of Objectification", 0),     CallState("Make Introspective Quill of Objectification", "Make Inscription of Aura of Blood Drinker Self"))
    #Rule("Make Inscription of Aura of Defender Self",      Condition_InventoryItemCountLE("Glyph of Melee Defense", 0),                     CallState("Make Glyph of Melee Defense",                 "Make Inscription of Aura of Blood Drinker Self"))
    #Rule("Make Inscription of Aura of Defender Self",      Condition_Always(),                                                              ExprAction("actiontryapplyitem[ wobjectfindininventorybyname[Introspective Quill of Objectification], wobjectfindininventorybyname[Glyph of Melee Defense]]"))
    #Rule("Make Inscription of Aura of Defender Self",      Condition_Always(),                                                              ReturnFromCall())

    Rule("Default",                                        Condition_Chat("!item"),                                                         CallState("MakeItemScrolls1", "Default"))
    Rule("MakeItemScrolls1",                               Condition_InventoryItemCountLE("Inscription of Aura of Blood Drinker Self", 0),  CallState("Make Inscription of Aura of Blood Drinker Self", "MakeItemScrolls2"))
    Rule("MakeItemScrolls1",                               Condition_Always(),                                                              SetMetaState("MakeItemScrolls2"))
    Rule("MakeItemScrolls2",                               Condition_InventoryItemCountLE("Inscription of Aura of Defender Self", 0),       CallState("Make Inscription of Aura of Defender Self",      "MakeItemScrolls3"))
    Rule("MakeItemScrolls2",                               Condition_Always(),                                                              SetMetaState("MakeItemScrolls3"))
    Rule("MakeItemScrolls3",                               Condition_Always(),                                                              SetMetaState("Default"))

def generate_meta(rules):
    print "1"
    print "CondAct"
    print "5"
    print "CType"
    print "AType"
    print "CData"
    print "AData"
    print "State"
    print "n"
    print "n"
    print "n"
    print "n"
    print "n"
    print len(rules)
    for rule in rules:
        if debug:
            print
            print "----------------------------------------------------------------------"
        rule.generate_meta()

#----------------------------------------------------------------------

#  Basic components: Mana Scarab, Quill of Introspection, Ink of Objectification, Glyph of Strength, Glyph of Melee Defense
#    Infused Quills: Infused Quill of Introspection
#  Third Step items: Introspective Quill of Objectifications
# Fourth step items: Inscription of Aura of Defender Self

rules = []

def BasicComponent(name):
    state = "Make %s" % name
    rules.append(Rule(state, Condition_Always(), AllCommand([ChatCommand("/s Need %s" % name),
                                                             SetMetaState("Default")
                                                             ])))
    #rules.append(Rule(state, Condition_Always(), ChatCommand("/s %s: Use %s" % (state, name))))
    #rules.append(Rule(state, Condition_Always(), ReturnFromCall()))

def Recipe(result, first, second, count = 1):
    state  = "Make %s" % result
    state2 = state + "2"
    state3 = state + "3"

    rules.append(Rule(state, Condition_All([#Condition_SecondsInStateGE(1),
                                            Condition_InventoryItemCountLE(result, count-1),
                                            Condition_InventoryItemCountLE(first, 0)
                                            ]),                                                       CallState("Make %s" % first,  state2)))
    rules.append(Rule(state, Condition_All([#Condition_SecondsInStateGE(1),
                                            Condition_Always()
                                            ]),                                                       SetMetaState(state2)))
    rules.append(Rule(state2, Condition_All([#Condition_SecondsInStateGE(1),
                                            Condition_InventoryItemCountLE(result, count-1),
                                            Condition_InventoryItemCountLE(second, 0)
                                            ]),                                                       CallState("Make %s" % second, state3)))
    rules.append(Rule(state2, Condition_All([#Condition_SecondsInStateGE(1),
                                            Condition_Always()
                                            ]),                                                       SetMetaState(state3)))
    rules.append(Rule(state3, Condition_All([Condition_SecondsInStateGE(1),
                                            Condition_InventoryItemCountLE(result, count-1),
                                            Condition_Not(Condition_InventoryItemCountLE(first, 0)),
                                            Condition_Not(Condition_InventoryItemCountLE(second, 0))
                                            ]),                                                       AllCommand([ExprAction("actiontryapplyitem[ wobjectfindininventorybyname[%s], wobjectfindininventorybyname[%s]]" % (first, second)),
                                                                                                                  #ReturnFromCall()
                                                                                                                  ])))
    rules.append(Rule(state3, Condition_All([Condition_SecondsInStateGE(2),
                                            Condition_InventoryItemCountLE(result, count-1),
                                            ]),                                                       SetMetaState(state)))
    #rules.append(Rule(state, Condition_SecondsInStateGE(1),                                           ReturnFromCall()))
    #rules.append(Rule(state, Condition_Chat("^You "),                                                 ReturnFromCall()))
    #rules.append(Rule(state, Condition_Not(Condition_InventoryItemCountLE(result, count-1)), ReturnFromCall()))
    rcmd = ReturnFromCall()
    if count > 1:
        rcmd = AllCommand([ChatCommand("Done making %d %s" % (count, result)),
                           ChatExpression("\\(+cstr[stopwatchelapsedseconds[getvar[timer_one]]]+\\ seconds\\)"),
                           ExprAction("stopwatchstop[getvar[timer_one]]"),
                           ReturnFromCall()
                           ])

    rules.append(Rule(state3, Condition_All([Condition_SecondsInStateGE(2),
                                             Condition_Not(Condition_InventoryItemCountLE(result, count-1))
                                             ]),                                                       rcmd))
    #rules.append(Rule(state3, Condition_All([Condition_SecondsInStateGE(2+3),
    #                                         Condition_Not(Condition_InventoryItemCountLE(result, count-1))
    #                                         ]),                                                       rcmd))
    #rules.append(Rule(state3, Condition_All([Condition_SecondsInStateGE(2+5),
    #                                         Condition_Not(Condition_InventoryItemCountLE(result, count-1))
    #                                         ]),                                                       rcmd))

    rules.append(Rule(state3, Condition_All([Condition_SecondsInStateGE(2+2),
                                             Condition_InventoryItemCountLE(result, count-1)
                                             ]),                                                       AllCommand([ChatCommand("timed out making %s (%d)" % (result, count)),
                                                                                                                  SetMetaState(state)])))
    # Does it need an always return?
# This that "always" is the problem -- change to inventory item count


def RecipeGroup(group, result, first, second, count = 1):
    group.append(result)
    Recipe(result, first, second, count)

def Command(name, state, items):
    index = 1
    rules.append(Rule("Default", Condition_Chat("^You say, \"%s\"$" % name), AllCommand([ExprAction("setvar[timer_one,stopwatchcreate[]];stopwatchstart[getvar[timer_one]]"),
                                                                   SetMetaState("%s%03d" % (state, index))
                                                                   ])))
    #rules.append(Rule(state, Condition_Always(), ChatCommand("/s Entered state %s" % state)))
    for idx, item in enumerate(items):
        substate = "%s%03d" % (state, index)
        next_substate = "%s%03d" % (state, index + 1)
        #rules.append(Rule(substate, Condition_Always(), ChatCommand("/s Making %s" % item)))
        rules.append(Rule(substate, Condition_Always(), AllCommand([ChatCommand("/c %d/%d: Making %s" % (idx+1, len(items), item)),
                                                                    CallState("Make %s" % item, next_substate)])))
        index += 1
    substate = "%s%03d" % (state, index)
    rules.append(Rule(substate, Condition_Always(), AllCommand([ChatCommand("Done " + name),
                                                                SetMetaState("Default")])))

if 1:
    BasicComponent("Mana Scarab")
    BasicComponent("Quill of Introspection")
    BasicComponent("Quill of Benevolence")
    BasicComponent("Quill of Infliction")
    BasicComponent("Quill of Extraction")

    BasicComponent("Ink of Objectification")
    BasicComponent("Ink of Nullification")
    BasicComponent("Ink of Conveyance")
    BasicComponent("Ink of Formation")

    BasicComponent("Parabolic Ink")
    BasicComponent("Ink of Partition")
    BasicComponent("Alacritous Ink")
    BasicComponent("Ink of Direction")
    BasicComponent("Ink of Separation")

    BasicComponent("Glyph of Strength")
    BasicComponent("Glyph of Endurance")
    BasicComponent("Glyph of Coordination")
    BasicComponent("Glyph of Quickness")
    BasicComponent("Glyph of Focus")
    BasicComponent("Glyph of Self")

    BasicComponent("Glyph of Armor")
    BasicComponent("Glyph of Corrosion")
    BasicComponent("Glyph of Slashing")
    BasicComponent("Glyph of Bludgeoning")
    BasicComponent("Glyph of Flame")
    BasicComponent("Glyph of Frost")
    BasicComponent("Glyph of Lightning")
    BasicComponent("Glyph of Piercing")

    BasicComponent("Glyph of Regeneration")
    BasicComponent("Glyph of Mana Regeneration")
    BasicComponent("Glyph of Stamina Regeneration")
    BasicComponent("Glyph of Health")
    BasicComponent("Glyph of Stamina")
    BasicComponent("Glyph of Mana")


    BasicComponent("Glyph of Alchemy")
    BasicComponent("Glyph of Arcane Lore")
    BasicComponent("Glyph of Salvaging")
    BasicComponent("Glyph of Armor Tinkering")
    BasicComponent("Glyph of Cooking")
    BasicComponent("Glyph of Creature Enchantment")
    BasicComponent("Glyph of Deception")
    BasicComponent("Glyph of Dirty Fighting")
    BasicComponent("Glyph of Dual Wield")
    BasicComponent("Glyph of Loyalty")
    BasicComponent("Glyph of Finesse Weapons")
    BasicComponent("Glyph of Fletching")
    BasicComponent("Glyph of Healing")
    BasicComponent("Glyph of Heavy Weapons")
    BasicComponent("Glyph of Melee Defense")
    BasicComponent("Glyph of Item Enchantment")
    BasicComponent("Glyph of Item Tinkering")
    BasicComponent("Glyph of Jump")
    BasicComponent("Glyph of Leadership")
    BasicComponent("Glyph of Life Magic")
    BasicComponent("Glyph of Light Weapons")
    BasicComponent("Glyph of Lockpick")
    BasicComponent("Glyph of Magic Item Tinkering")
    BasicComponent("Glyph of Magic Defense")
    BasicComponent("Glyph of Mana Conversion")
    BasicComponent("Glyph of Missile Weapons")
    BasicComponent("Glyph of Monster Appraisal")
    BasicComponent("Glyph of Person Appraisal")
    BasicComponent("Glyph of Recklessness")
    BasicComponent("Glyph of Shield")
    BasicComponent("Glyph of Sneak Attack")
    BasicComponent("Glyph of Run")
    BasicComponent("Glyph of Two Handed Combat")
    BasicComponent("Glyph of Summoning")
    BasicComponent("Glyph of Void Magic")
    BasicComponent("Glyph of War Magic")
    BasicComponent("Glyph of Weapon Tinkering")

    Recipe("Infused Quill of Introspection",               "Quill of Introspection", "Mana Scarab")
    Recipe("Infused Quill of Benevolence",                 "Quill of Benevolence",   "Mana Scarab")
    Recipe("Infused Quill of Infliction",                  "Quill of Infliction",    "Mana Scarab")
    Recipe("Infused Quill of Extraction",                  "Quill of Extraction",    "Mana Scarab")

    Recipe("Introspective Quill of Formation",             "Infused Quill of Introspection", "Ink of Formation")
    Recipe("Introspective Quill of Nullification",         "Infused Quill of Introspection", "Ink of Nullification")
    Recipe("Introspective Quill of Objectification",       "Infused Quill of Introspection", "Ink of Objectification")
    Recipe("Benevolent Quill of Conveyance",               "Infused Quill of Benevolence",   "Ink of Conveyance")
    Recipe("Benevolent Quill of Nullification",            "Infused Quill of Benevolence",   "Ink of Nullification")
    Recipe("Benevolent Quill of Objectification",          "Infused Quill of Benevolence",   "Ink of Objectification")
    Recipe("Inflictive Quill of Conveyance",               "Infused Quill of Infliction",    "Ink of Conveyance")
    Recipe("Inflictive Quill of Objectification",          "Infused Quill of Infliction",    "Ink of Objectification")
    Recipe("Extracting Quill of Conveyance",               "Infused Quill of Extraction",    "Ink of Conveyance")

    Recipe("Extracting Quill of Direction",                "Infused Quill of Extraction",    "Ink of Direction") # For void
    Recipe("Extracting Quill of Partition",                "Infused Quill of Extraction",    "Ink of Partition")
    Recipe("Extracting Quill of Conveyance",               "Infused Quill of Extraction",    "Ink of Conveyance")
    Recipe("Extracting Quill of Nullification",            "Infused Quill of Extraction",    "Ink of Nullification")

    Recipe("Parabolic Quill of Infliction",                "Infused Quill of Infliction",    "Parabolic Ink")
    Recipe("Inflictive Quill of Direction",                "Infused Quill of Infliction",    "Ink of Direction")
    Recipe("Alacritous Quill of Infliction",               "Infused Quill of Infliction",    "Alacritous Ink")
    Recipe("Inflictive Quill of Partition",                "Infused Quill of Infliction",    "Ink of Partition")
    Recipe("Inflictive Quill of Separation",               "Infused Quill of Infliction",    "Ink of Separation")

    item_self = []

    RecipeGroup(item_self, "Inscription of Aura of Blood Drinker Self",    "Introspective Quill of Objectification", "Glyph of Strength")
    RecipeGroup(item_self, "Inscription of Aura of Defender Self",         "Introspective Quill of Objectification", "Glyph of Melee Defense")
    RecipeGroup(item_self, "Inscription of Aura of Heart Seeker Self",     "Introspective Quill of Objectification", "Glyph of Coordination")
    RecipeGroup(item_self, "Inscription of Aura of Hermetic Link Self",    "Introspective Quill of Objectification", "Glyph of Mana Conversion")
    RecipeGroup(item_self, "Inscription of Aura of Spirit Drinker Self",   "Introspective Quill of Objectification", "Glyph of Focus")
    RecipeGroup(item_self, "Inscription of Swift Killer Self",             "Introspective Quill of Objectification", "Glyph of Quickness")

    RecipeGroup(item_self, "Inscription of Impenetrability",               "Benevolent Quill of Objectification", "Glyph of Armor")
    RecipeGroup(item_self, "Inscription of Acid Bane",                     "Benevolent Quill of Objectification", "Glyph of Corrosion")
    RecipeGroup(item_self, "Inscription of Blade Bane",                    "Benevolent Quill of Objectification", "Glyph of Slashing")
    RecipeGroup(item_self, "Inscription of Bludgeon Bane",                 "Benevolent Quill of Objectification", "Glyph of Bludgeoning")
    RecipeGroup(item_self, "Inscription of Flame Bane",                    "Benevolent Quill of Objectification", "Glyph of Flame")
    RecipeGroup(item_self, "Inscription of Frost Bane",                    "Benevolent Quill of Objectification", "Glyph of Frost")
    RecipeGroup(item_self, "Inscription of Lightning Bane",                "Benevolent Quill of Objectification", "Glyph of Lightning")
    RecipeGroup(item_self, "Inscription of Piercing Bane",                 "Benevolent Quill of Objectification", "Glyph of Piercing")
    RecipeGroup(item_self, "Inscription of Nullify Item Magic",            "Introspective Quill of Nullification", "Glyph of Item Enchantment")

    Command("!item self", "MakeItemSelfScrolls", item_self)

    item_other = []

    RecipeGroup(item_other, "Inscription of Aura of Blood Drinker Other",   "Benevolent Quill of Objectification", "Glyph of Strength")
    RecipeGroup(item_other, "Inscription of Aura of Defender Other",        "Benevolent Quill of Objectification", "Glyph of Melee Defense")
    RecipeGroup(item_other, "Inscription of Aura of Heart Seeker Other",    "Benevolent Quill of Objectification", "Glyph of Coordination")
    RecipeGroup(item_other, "Inscription of Aura of Hermetic Link Other",   "Benevolent Quill of Objectification", "Glyph of Mana Conversion")
    RecipeGroup(item_other, "Inscription of Aura of Spirit Drinker Other",  "Benevolent Quill of Objectification", "Glyph of Focus")
    RecipeGroup(item_other, "Inscription of Swift Killer Other",            "Benevolent Quill of Objectification", "Glyph of Quickness")

    RecipeGroup(item_other, "Inscription of Acid Lure",                     "Inflictive Quill of Objectification", "Glyph of Corrosion")
    RecipeGroup(item_other, "Inscription of Blade Lure",                    "Inflictive Quill of Objectification", "Glyph of Slashing")
    RecipeGroup(item_other, "Inscription of Bludgeon Lure",                 "Inflictive Quill of Objectification", "Glyph of Bludgeoning")
    RecipeGroup(item_other, "Inscription of Flame Lure",                    "Inflictive Quill of Objectification", "Glyph of Flame")
    RecipeGroup(item_other, "Inscription of Frost Lure",                    "Inflictive Quill of Objectification", "Glyph of Frost")
    RecipeGroup(item_other, "Inscription of Lightning Lure",                "Inflictive Quill of Objectification", "Glyph of Lightning")
    RecipeGroup(item_other, "Inscription of Piercing Lure",                 "Inflictive Quill of Objectification", "Glyph of Piercing")
    RecipeGroup(item_other, "Inscription of Blood Loather",                 "Inflictive Quill of Objectification", "Glyph of Strength")
    RecipeGroup(item_other, "Inscription of Brittlemail",                   "Inflictive Quill of Objectification", "Glyph of Armor")
    RecipeGroup(item_other, "Inscription of Hermetic Void",                 "Inflictive Quill of Objectification", "Glyph of Mana Conversion")
    RecipeGroup(item_other, "Inscription of Leaden Weapon",                 "Inflictive Quill of Objectification", "Glyph of Quickness")
    RecipeGroup(item_other, "Inscription of Lure Blade",                    "Inflictive Quill of Objectification", "Glyph of Melee Defense")
    RecipeGroup(item_other, "Inscription of Spirit Loather",                "Inflictive Quill of Objectification", "Glyph of Focus")
    RecipeGroup(item_other, "Inscription of Turn Blade",                    "Inflictive Quill of Objectification", "Glyph of Coordination")
    RecipeGroup(item_other, "Inscription of Strengthen Lock",               "Benevolent Quill of Objectification", "Glyph of Lockpick")
    RecipeGroup(item_other, "Inscription of Weaken Lock",                   "Inflictive Quill of Objectification", "Glyph of Lockpick")

    Command("!item other", "MakeItemOtherScrolls", item_other)

    life = []

    RecipeGroup(life, "Inscription of Armor Self",                      "Introspective Quill of Formation",     "Glyph of Armor")
    RecipeGroup(life, "Inscription of Acid Protection Self",            "Introspective Quill of Formation",     "Glyph of Corrosion")
    RecipeGroup(life, "Inscription of Blade Protection Self",           "Introspective Quill of Formation",     "Glyph of Slashing")
    RecipeGroup(life, "Inscription of Bludgeoning Protection Self",     "Introspective Quill of Formation",     "Glyph of Bludgeoning")
    RecipeGroup(life, "Inscription of Cold Protection Self",            "Introspective Quill of Formation",     "Glyph of Frost")
    RecipeGroup(life, "Inscription of Fire Protection Self",            "Introspective Quill of Formation",     "Glyph of Flame")
    RecipeGroup(life, "Inscription of Lightning Protection Self",       "Introspective Quill of Formation",     "Glyph of Lightning")
    RecipeGroup(life, "Inscription of Piercing Protection Self",        "Introspective Quill of Formation",     "Glyph of Piercing")

    RecipeGroup(life, "Inscription of Acid Vulnerability Other",        "Inflictive Quill of Conveyance",       "Glyph of Corrosion")
    RecipeGroup(life, "Inscription of Blade Vulnerability Other",       "Inflictive Quill of Conveyance",       "Glyph of Slashing")
    RecipeGroup(life, "Inscription of Bludgeoning Vulnerability Other", "Inflictive Quill of Conveyance",       "Glyph of Bludgeoning")
    RecipeGroup(life, "Inscription of Cold Vulnerability Other",        "Inflictive Quill of Conveyance",       "Glyph of Frost")
    RecipeGroup(life, "Inscription of Fire Vulnerability Other",        "Inflictive Quill of Conveyance",       "Glyph of Flame")
    RecipeGroup(life, "Inscription of Lightning Vulnerability Other",   "Inflictive Quill of Conveyance",       "Glyph of Lightning")
    RecipeGroup(life, "Inscription of Piercing Vulnerability Other",    "Inflictive Quill of Conveyance",       "Glyph of Piercing")

    RecipeGroup(life, "Inscription of Drain Health Other",              "Extracting Quill of Conveyance",       "Glyph of Health")
    RecipeGroup(life, "Inscription of Drain Mana Other",                "Extracting Quill of Conveyance",       "Glyph of Mana")
    RecipeGroup(life, "Inscription of Drain Stamina Other",             "Extracting Quill of Conveyance",       "Glyph of Stamina")
    RecipeGroup(life, "Inscription of Enfeeble Other",                  "Inflictive Quill of Conveyance",       "Glyph of Stamina")
    RecipeGroup(life, "Inscription of Exhaustion Other",                "Inflictive Quill of Conveyance",       "Glyph of Stamina Regeneration")
    RecipeGroup(life, "Inscription of Fester Other",                    "Inflictive Quill of Conveyance",       "Glyph of Regeneration")
    RecipeGroup(life, "Inscription of Harm Other",                      "Inflictive Quill of Conveyance",       "Glyph of Health")
    RecipeGroup(life, "Inscription of Heal Self",                       "Introspective Quill of Formation",     "Glyph of Health")
    RecipeGroup(life, "Inscription of Heal Other",                      "Benevolent Quill of Conveyance",       "Glyph of Health")
    RecipeGroup(life, "Inscription of Mana Depletion Other",            "Inflictive Quill of Conveyance",       "Glyph of Mana Regeneration")
    RecipeGroup(life, "Inscription of Mana Drain Other",                "Inflictive Quill of Conveyance",       "Glyph of Mana")
    RecipeGroup(life, "Inscription of Mana Renewal Self",               "Introspective Quill of Formation",     "Glyph of Mana Regeneration")
    RecipeGroup(life, "Inscription of Regeneration Self",               "Introspective Quill of Formation",     "Glyph of Regeneration")
    RecipeGroup(life, "Inscription of Revitalize Other",                "Benevolent Quill of Conveyance",       "Glyph of Stamina")
    RecipeGroup(life, "Inscription of Rejuvenation Self",               "Introspective Quill of Formation",     "Glyph of Stamina Regeneration")
    RecipeGroup(life, "Inscription of Revitalize Self",                 "Introspective Quill of Formation",     "Glyph of Stamina")

    RecipeGroup(life, "Inscription of Nullify Life Magic Other",        "Benevolent Quill of Nullification",    "Glyph of Life Magic")
    RecipeGroup(life, "Inscription of Nullify Life Magic Self",         "Introspective Quill of Nullification", "Glyph of Life Magic")

    Command("!life", "MakeLifeScrolls", life)

    creature_self = []

    RecipeGroup(creature_self, "Inscription of Strength Self",     "Introspective Quill of Formation", "Glyph of Strength")
    RecipeGroup(creature_self, "Inscription of Endurance Self",    "Introspective Quill of Formation", "Glyph of Endurance")
    RecipeGroup(creature_self, "Inscription of Coordination Self", "Introspective Quill of Formation", "Glyph of Coordination")
    RecipeGroup(creature_self, "Inscription of Quickness Self",    "Introspective Quill of Formation", "Glyph of Quickness")
    RecipeGroup(creature_self, "Inscription of Focus Self",        "Introspective Quill of Formation", "Glyph of Focus")
    RecipeGroup(creature_self, "Inscription of Willpower Self",    "Introspective Quill of Formation", "Glyph of Self")

    RecipeGroup(creature_self, "Inscription of Alchemy Mastery Self",                "Introspective Quill of Formation", "Glyph of Alchemy")
    RecipeGroup(creature_self, "Inscription of Arcane Enlightenment Self",           "Introspective Quill of Formation", "Glyph of Arcane Lore")
    RecipeGroup(creature_self, "Inscription of Arcanum Salvaging Self",              "Introspective Quill of Formation", "Glyph of Salvaging")
    RecipeGroup(creature_self, "Inscription of Armor Tinkering Expertise Self",      "Introspective Quill of Formation", "Glyph of Armor Tinkering")
    RecipeGroup(creature_self, "Inscription of Cooking Mastery Self",                "Introspective Quill of Formation", "Glyph of Cooking")
    RecipeGroup(creature_self, "Inscription of Creature Enchantment Mastery Self",   "Introspective Quill of Formation", "Glyph of Creature Enchantment")
    RecipeGroup(creature_self, "Inscription of Deception Mastery Self",              "Introspective Quill of Formation", "Glyph of Deception")
    RecipeGroup(creature_self, "Inscription of Dirty Fighting Mastery Self",         "Introspective Quill of Formation", "Glyph of Dirty Fighting")
    RecipeGroup(creature_self, "Inscription of Dual Wield Mastery Self",             "Introspective Quill of Formation", "Glyph of Dual Wield")
    RecipeGroup(creature_self, "Inscription of Fealty Self",                         "Introspective Quill of Formation", "Glyph of Loyalty")
    RecipeGroup(creature_self, "Inscription of Finesse Weapon Mastery Self",         "Introspective Quill of Formation", "Glyph of Finesse Weapons")
    RecipeGroup(creature_self, "Inscription of Fletching Mastery Self",              "Introspective Quill of Formation", "Glyph of Fletching")
    RecipeGroup(creature_self, "Inscription of Healing Mastery Self",                "Introspective Quill of Formation", "Glyph of Healing")
    RecipeGroup(creature_self, "Inscription of Heavy Weapon Mastery Self",           "Introspective Quill of Formation", "Glyph of Heavy Weapons")
    RecipeGroup(creature_self, "Inscription of Invulnerability Self",                "Introspective Quill of Formation", "Glyph of Melee Defense")
    RecipeGroup(creature_self, "Inscription of Impregnability Self",                 "Introspective Quill of Formation", "Glyph of Missile Defense")
    RecipeGroup(creature_self, "Inscription of Item Enchantment Mastery Self",       "Introspective Quill of Formation", "Glyph of Item Enchantment")
    RecipeGroup(creature_self, "Inscription of Item Tinkering Expertise Self",       "Introspective Quill of Formation", "Glyph of Item Tinkering")
    RecipeGroup(creature_self, "Inscription of Jumping Mastery Self",                "Introspective Quill of Formation", "Glyph of Jump")
    RecipeGroup(creature_self, "Inscription of Leadership Mastery Self",             "Introspective Quill of Formation", "Glyph of Leadership")
    RecipeGroup(creature_self, "Inscription of Life Magic Mastery Self",             "Introspective Quill of Formation", "Glyph of Life Magic")
    RecipeGroup(creature_self, "Inscription of Light Weapon Mastery Self",           "Introspective Quill of Formation", "Glyph of Light Weapons")
    RecipeGroup(creature_self, "Inscription of Lockpick Mastery Self",               "Introspective Quill of Formation", "Glyph of Lockpick")
    RecipeGroup(creature_self, "Inscription of Magic Item Tinkering Expertise Self", "Introspective Quill of Formation", "Glyph of Magic Item Tinkering")
    RecipeGroup(creature_self, "Inscription of Magic Resistance Self",               "Introspective Quill of Formation", "Glyph of Magic Defense")
    RecipeGroup(creature_self, "Inscription of Mana Conversion Mastery Self",        "Introspective Quill of Formation", "Glyph of Mana Conversion")
    RecipeGroup(creature_self, "Inscription of Missile Weapon Mastery Self",         "Introspective Quill of Formation", "Glyph of Missile Weapons")
    RecipeGroup(creature_self, "Inscription of Monster Attunement Self",             "Introspective Quill of Formation", "Glyph of Monster Appraisal")
    RecipeGroup(creature_self, "Inscription of Person Attunement Self",              "Introspective Quill of Formation", "Glyph of Person Appraisal")
    RecipeGroup(creature_self, "Inscription of Recklessness Mastery Self",           "Introspective Quill of Formation", "Glyph of Recklessness")
    RecipeGroup(creature_self, "Inscription of Shield Mastery Self",                 "Introspective Quill of Formation", "Glyph of Shield")
    RecipeGroup(creature_self, "Inscription of Sneak Attack Mastery Self",           "Introspective Quill of Formation", "Glyph of Sneak Attack")
    RecipeGroup(creature_self, "Inscription of Sprint Self",                         "Introspective Quill of Formation", "Glyph of Run")
    RecipeGroup(creature_self, "Scroll of Two Handed Weapon Mastery Self VIII",      "Introspective Quill of Formation", "Glyph of Two Handed Combat")
    RecipeGroup(creature_self, "Inscription of Summoning Mastery Self",              "Introspective Quill of Formation", "Glyph of Summoning")
    RecipeGroup(creature_self, "Inscription of Void Magic Mastery Self",             "Introspective Quill of Formation", "Glyph of Void Magic")
    RecipeGroup(creature_self, "Inscription of War Magic Mastery Self",              "Introspective Quill of Formation", "Glyph of War Magic")
    RecipeGroup(creature_self, "Inscription of Weapon Tinkering Expertise Self",     "Introspective Quill of Formation", "Glyph of Weapon Tinkering")

    RecipeGroup(creature_self, "Inscription of Nullify Creature Magic Self", "Introspective Quill of Nullification", "Glyph of Creature Enchantment")

    Command("!creature self", "MakeCreatureSelfScrolls", creature_self)

    creature_other = []

    RecipeGroup(creature_other, "Inscription of Weakness Other",   "Inflictive Quill of Conveyance", "Glyph of Strength")
    RecipeGroup(creature_other, "Inscription of Frailty Other",    "Inflictive Quill of Conveyance", "Glyph of Endurance")
    RecipeGroup(creature_other, "Inscription of Clumsiness Other", "Inflictive Quill of Conveyance", "Glyph of Coordination")
    RecipeGroup(creature_other, "Inscription of Slowness Other",   "Inflictive Quill of Conveyance", "Glyph of Quickness")
    RecipeGroup(creature_other, "Inscription of Bafflement Other", "Inflictive Quill of Conveyance", "Glyph of Focus")
    RecipeGroup(creature_other, "Inscription of Feeblemind Other", "Inflictive Quill of Conveyance", "Glyph of Self")

    RecipeGroup(creature_other, "Inscription of Alchemy Ineptitude Other",              "Inflictive Quill of Conveyance", "Glyph of Alchemy")
    RecipeGroup(creature_other, "Inscription of Arcane Benightedness Other",            "Inflictive Quill of Conveyance", "Glyph of Arcane Lore")
    #RecipeGroup(creature_other, "Inscription of Arcanum Salvaging Other",               "Inflictive Quill of Conveyance", "Glyph of Salvaging")
    RecipeGroup(creature_other, "Inscription of Armor Tinkering Ignorance Other",       "Inflictive Quill of Conveyance", "Glyph of Armor Tinkering")
    RecipeGroup(creature_other, "Inscription of Cooking Ineptitude Other",              "Inflictive Quill of Conveyance", "Glyph of Cooking")
    RecipeGroup(creature_other, "Inscription of Creature Enchantment Ineptitude Other", "Inflictive Quill of Conveyance", "Glyph of Creature Enchantment")
    RecipeGroup(creature_other, "Inscription of Deception Ineptitude Other",            "Inflictive Quill of Conveyance", "Glyph of Deception")
    RecipeGroup(creature_other, "Inscription of Dirty Fighting Ineptitude Other",       "Inflictive Quill of Conveyance", "Glyph of Dirty Fighting")
    RecipeGroup(creature_other, "Inscription of Dual Wield Ineptitude Other",           "Inflictive Quill of Conveyance", "Glyph of Dual Wield")
    RecipeGroup(creature_other, "Inscription of Faithlessness Other",                   "Inflictive Quill of Conveyance", "Glyph of Loyalty")
    RecipeGroup(creature_other, "Inscription of Finesse Weapon Ineptitude Other",       "Inflictive Quill of Conveyance", "Glyph of Finesse Weapons")
    RecipeGroup(creature_other, "Inscription of Fletching Ineptitude Other",            "Inflictive Quill of Conveyance", "Glyph of Fletching")
    RecipeGroup(creature_other, "Inscription of Healing Ineptitude Other",              "Inflictive Quill of Conveyance", "Glyph of Healing")
    RecipeGroup(creature_other, "Inscription of Heavy Weapon Ineptitude Other",         "Inflictive Quill of Conveyance", "Glyph of Heavy Weapons")
    RecipeGroup(creature_other, "Inscription of Vulnerability Other",                   "Inflictive Quill of Conveyance", "Glyph of Melee Defense")
    RecipeGroup(creature_other, "Inscription of Defenselessness Other",                 "Inflictive Quill of Conveyance", "Glyph of Missile Defense")
    RecipeGroup(creature_other, "Inscription of Item Enchantment Ineptitude Other",     "Inflictive Quill of Conveyance", "Glyph of Item Enchantment")
    RecipeGroup(creature_other, "Inscription of Item Tinkering Ignorance Other",        "Inflictive Quill of Conveyance", "Glyph of Item Tinkering")
    RecipeGroup(creature_other, "Inscription of Jumping Ineptitude Other",              "Inflictive Quill of Conveyance", "Glyph of Jump") # *** wiki wrong, calls it self
    RecipeGroup(creature_other, "Inscription of Leadership Ineptitude Other",           "Inflictive Quill of Conveyance", "Glyph of Leadership")
    RecipeGroup(creature_other, "Inscription of Life Magic Ineptitude Other",           "Inflictive Quill of Conveyance", "Glyph of Life Magic")
    RecipeGroup(creature_other, "Inscription of Light Weapon Ineptitude Other",         "Inflictive Quill of Conveyance", "Glyph of Light Weapons")
    RecipeGroup(creature_other, "Inscription of Lockpick Ineptitude Other",             "Inflictive Quill of Conveyance", "Glyph of Lockpick")
    RecipeGroup(creature_other, "Inscription of Magic Item Tinkering Ignorance Other",  "Inflictive Quill of Conveyance", "Glyph of Magic Item Tinkering")
    RecipeGroup(creature_other, "Inscription of Magic Yield Other",                     "Inflictive Quill of Conveyance", "Glyph of Magic Defense")
    RecipeGroup(creature_other, "Inscription of Mana Conversion Ineptitude Other",      "Inflictive Quill of Conveyance", "Glyph of Mana Conversion")
    RecipeGroup(creature_other, "Inscription of Missile Weapon Ineptitude Other",       "Inflictive Quill of Conveyance", "Glyph of Missile Weapons")
    RecipeGroup(creature_other, "Inscription of Monster Unfamiliarity Other",           "Inflictive Quill of Conveyance", "Glyph of Monster Appraisal")
    RecipeGroup(creature_other, "Inscription of Person Unfamiliarity Other",            "Inflictive Quill of Conveyance", "Glyph of Person Appraisal")
    RecipeGroup(creature_other, "Inscription of Recklessness Ineptitude Other",         "Inflictive Quill of Conveyance", "Glyph of Recklessness")
    RecipeGroup(creature_other, "Inscription of Shield Ineptitude Other",               "Inflictive Quill of Conveyance", "Glyph of Shield")
    RecipeGroup(creature_other, "Inscription of Sneak Attack Ineptitude Other",         "Inflictive Quill of Conveyance", "Glyph of Sneak Attack")
    RecipeGroup(creature_other, "Inscription of Leaden Feet Other",                     "Inflictive Quill of Conveyance", "Glyph of Run")
    RecipeGroup(creature_other, "Scroll of Two Handed Weapons Ineptitude VIII",         "Inflictive Quill of Conveyance", "Glyph of Two Handed Combat")
    RecipeGroup(creature_other, "Inscription of Summoning Ineptitude Other",            "Inflictive Quill of Conveyance", "Glyph of Summoning")
    RecipeGroup(creature_other, "Inscription of Void Magic Ineptitude Other",           "Inflictive Quill of Conveyance", "Glyph of Void Magic")
    RecipeGroup(creature_other, "Inscription of War Magic Ineptitude Other",            "Inflictive Quill of Conveyance", "Glyph of War Magic")
    RecipeGroup(creature_other, "Inscription of Weapon Tinkering Ignorance Other",      "Inflictive Quill of Conveyance", "Glyph of Weapon Tinkering")

    RecipeGroup(creature_other, "Inscription of Nullify Creature Magic Other", "Benevolent Quill of Nullification", "Glyph of Creature Enchantment")

    Command("!creature other", "MakeCreatureOtherScrolls", creature_other)

    war = []

    RecipeGroup(war, "Inscription of Acid Arc",      "Parabolic Quill of Infliction", "Glyph of Corrosion")
    RecipeGroup(war, "Inscription of Blade Arc",     "Parabolic Quill of Infliction", "Glyph of Slashing")
    RecipeGroup(war, "Inscription of Shock Arc",     "Parabolic Quill of Infliction", "Glyph of Bludgeoning")
    RecipeGroup(war, "Inscription of Flame Arc",     "Parabolic Quill of Infliction", "Glyph of Flame")
    RecipeGroup(war, "Inscription of Frost Arc",     "Parabolic Quill of Infliction", "Glyph of Frost")
    RecipeGroup(war, "Inscription of Lightning Arc", "Parabolic Quill of Infliction", "Glyph of Lightning")
    RecipeGroup(war, "Inscription of Force Arc",     "Parabolic Quill of Infliction", "Glyph of Piercing")

    RecipeGroup(war, "Inscription of Acid Stream",    "Inflictive Quill of Direction", "Glyph of Corrosion")
    RecipeGroup(war, "Inscription of Whirling Blade", "Inflictive Quill of Direction", "Glyph of Slashing")
    RecipeGroup(war, "Inscription of Shock Wave",     "Inflictive Quill of Direction", "Glyph of Bludgeoning")
    RecipeGroup(war, "Inscription of Flame Bolt",     "Inflictive Quill of Direction", "Glyph of Flame")
    RecipeGroup(war, "Inscription of Frost Bolt",     "Inflictive Quill of Direction", "Glyph of Frost")
    RecipeGroup(war, "Inscription of Lightning Bolt", "Inflictive Quill of Direction", "Glyph of Lightning")
    RecipeGroup(war, "Inscription of Force Bolt",     "Inflictive Quill of Direction", "Glyph of Piercing")

    RecipeGroup(war, "Inscription of Acid Streak",           "Alacritous Quill of Infliction", "Glyph of Corrosion")
    RecipeGroup(war, "Inscription of Whirling Blade Streak", "Alacritous Quill of Infliction", "Glyph of Slashing")
    RecipeGroup(war, "Inscription of Shock Wave Streak",     "Alacritous Quill of Infliction", "Glyph of Bludgeoning")
    RecipeGroup(war, "Inscription of Flame Streak",          "Alacritous Quill of Infliction", "Glyph of Flame")
    RecipeGroup(war, "Inscription of Frost Streak",          "Alacritous Quill of Infliction", "Glyph of Frost")
    RecipeGroup(war, "Inscription of Lightning Streak",      "Alacritous Quill of Infliction", "Glyph of Lightning")
    RecipeGroup(war, "Inscription of Force Streak",          "Alacritous Quill of Infliction", "Glyph of Piercing")

    RecipeGroup(war, "Inscription of Acid Blast",      "Inflictive Quill of Partition", "Glyph of Corrosion")
    RecipeGroup(war, "Inscription of Blade Blast",     "Inflictive Quill of Partition", "Glyph of Slashing")
    RecipeGroup(war, "Inscription of Shock Blast",     "Inflictive Quill of Partition", "Glyph of Bludgeoning")
    RecipeGroup(war, "Inscription of Flame Blast",     "Inflictive Quill of Partition", "Glyph of Flame")
    RecipeGroup(war, "Inscription of Frost Blast",     "Inflictive Quill of Partition", "Glyph of Frost")
    RecipeGroup(war, "Inscription of Lightning Blast", "Inflictive Quill of Partition", "Glyph of Lightning")
    RecipeGroup(war, "Inscription of Force Blast",     "Inflictive Quill of Partition", "Glyph of Piercing")

    RecipeGroup(war, "Inscription of Acid Volley",        "Inflictive Quill of Separation", "Glyph of Corrosion")
    RecipeGroup(war, "Inscription of Blade Volley",       "Inflictive Quill of Separation", "Glyph of Slashing")
    RecipeGroup(war, "Inscription of Bludgeoning Volley", "Inflictive Quill of Separation", "Glyph of Bludgeoning")
    RecipeGroup(war, "Inscription of Flame Volley",       "Inflictive Quill of Separation", "Glyph of Flame")
    RecipeGroup(war, "Inscription of Frost Volley",       "Inflictive Quill of Separation", "Glyph of Frost")
    RecipeGroup(war, "Inscription of Lightning Volley",   "Inflictive Quill of Separation", "Glyph of Lightning")
    RecipeGroup(war, "Inscription of Force Volley",       "Inflictive Quill of Separation", "Glyph of Piercing")

    Command("!war", "MakeWarScrolls", war)

    void = []

    RecipeGroup(void, "Inscription of Corrosion",         "Extracting Quill of Direction",     "Glyph of Nether")
    RecipeGroup(void, "Inscription of Corruption",        "Extracting Quill of Partition",     "Glyph of Nether")
    RecipeGroup(void, "Inscription of Destructive Curse", "Extracting Quill of Conveyance",    "Glyph of Nether")
    RecipeGroup(void, "Inscription of Festering Curse",   "Extracting Quill of Nullification", "Glyph of Healing")

    RecipeGroup(void, "Inscription of Nether Arc",        "Parabolic Quill of Infliction",     "Glyph of Nether")
    RecipeGroup(void, "Inscription of Nether Blast",      "Inflictive Quill of Partition",     "Glyph of Nether")
    RecipeGroup(void, "Inscription of Nether Bolt",       "Inflictive Quill of Direction",     "Glyph of Nether")
    RecipeGroup(void, "Inscription of Nether Streak",     "Alacritous Quill of Infliction",    "Glyph of Nether")
    RecipeGroup(void, "Inscription of Weakening Curse",   "Extracting Quill of Nullification", "Glyph of Damage")

    Command("!void", "MakeVoidScrolls", void)


    rules.append(Rule("Default", Condition_Chat("!stop"), AllCommand([ChatCommand("Switching to test2"),
                                                                      ChatCommand("/vt meta load test2")
                                                                      ])))

    melee = []
    RecipeGroup(melee, "Inscription of Aura of Defender Self",         "Introspective Quill of Objectification", "Glyph of Melee Defense")
    RecipeGroup(melee, "Inscription of Aura of Defender Other",        "Benevolent Quill of Objectification", "Glyph of Melee Defense")
    RecipeGroup(melee, "Inscription of Lure Blade",                    "Inflictive Quill of Objectification", "Glyph of Melee Defense")
    RecipeGroup(melee, "Inscription of Invulnerability Self",                "Introspective Quill of Formation", "Glyph of Melee Defense")
    RecipeGroup(melee, "Inscription of Vulnerability Other",                   "Inflictive Quill of Conveyance", "Glyph of Melee Defense")
    Command("!melee", "MakeMelee", melee)

if 0:
    BasicComponent("Water")
    BasicComponent("Plain Barley")
    BasicComponent("Amber Barley")

    BasicComponent("Ultra Green Hops")
    BasicComponent("Dried Yeast")

    BasicComponent("Brew Kettle")
    BasicComponent("Baking Pan")
    BasicComponent("Tusker Spit")
    BasicComponent("Moarsmuck")
    #BasicComponent("Empty Stopped Keg")
    #BasicComponent("Empty Bottles")

    Recipe("Full Brew Kettle",               "Brew Kettle",      "Water")
    Recipe("Roasted Barley",                 "Baking Pan",       "Plain Barley")

    # Coordination
    Recipe("Amber Ape Brew",                 "Tusker Spit",      "Glorious Amber Brew", 5)
    # Endurance
    Recipe("Hunter's Stock Amber Brew",      "Moarsmuck",        "Glorious Amber Brew", 5)

    Recipe("Glorious Amber Brew",            "Dried Yeast",      "Aromatic Amber Wort");
    Recipe("Aromatic Amber Wort",            "Ultra Green Hops", "Amber Wort");
    Recipe("Amber Wort",                     "Amber Barley",     "Full Brew Kettle")


    # Strength
    Recipe("Apothecary Zongo's Stout Brew",  "Moarsmuck",        "Glorious Dark Brew", 5)
    # Quickness
    Recipe("Bobo's Stout Brew",              "Tusker Spit",      "Glorious Dark Brew", 5)

    Recipe("Glorious Dark Brew",             "Dried Yeast",      "Aromatic Dark Wort")
    Recipe("Aromatic Dark Wort",             "Ultra Green Hops", "Dark Wort")
    Recipe("Dark Wort",                      "Roasted Barley",   "Full Brew Kettle")


    # Willpower
    Recipe("Duke Raoul's Distillation Brew", "Moarsmuck",        "Glorious Fermented Brew", 5)
    # Focus
    Recipe("Tusker Spit Brew",               "Tusker Spit",      "Glorious Fermented Brew", 5)

    Recipe("Glorious Fermented Brew",        "Dried Yeast",      "Aromatic Finished Wort")
    Recipe("Aromatic Finished Wort",         "Ultra Green Hops", "Sweet Wort")
    Recipe("Sweet Wort",                     "Plain Barley",     "Full Brew Kettle")




    #rules.append(Rule("Default", Condition_Chat("!go"), AllCommand([ExprAction("setvar[timer_one,stopwatchcreate[]];stopwatchstart[getvar[timer_one]]"),
    #                                                                CallState("Make Glorious Fermented Brew", "Default"
    #                                                                          ]))))
    Command("!go", "MakeBeer", ["Amber Ape Brew", "Hunter's Stock Amber Brew", "Apothecary Zongo's Stout Brew", "Bobo's Stout Brew", "Duke Raoul's Distillation Brew", "Tusker Spit Brew"])

    rules.append(Rule("Default", Condition_Chat("!stop"), AllCommand([ChatCommand("Switching to test2"),
                                                                      ChatCommand("/vt meta load test2")
                                                                      ])))

if 0:
    rules.append(Rule("Default", Condition_All([Condition_Chat("!go"),
                                                Condition_InventoryItemCountLE("Water", 77)
                                                ]),
                      ChatCommand("/s ok")))

generate_meta(rules)
